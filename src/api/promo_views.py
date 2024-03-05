import re

from django_filters import rest_framework as rf_filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, response, status, viewsets
from rest_framework.decorators import action

from .filters import MerchApplicationsFilter
from .permissions import IsTutorOrReadOnly
from .promo_serializers import (
    MerchApplicationCreateUpdateSerializer,
    MerchApplicationSerializer,
    YearBudgetSerializer,
)
from .utils import generate_application_number
from ambassadors.models import Ambassador
from promo.models import MerchApplication

YEAR_MONTHS = [
    ("january", 1),
    ("february", 2),
    ("march", 3),
    ("april", 4),
    ("may", 5),
    ("june", 6),
    ("july", 7),
    ("august", 8),
    ("september", 9),
    ("october", 10),
    ("november", 11),
    ("december", 12),
]

year = openapi.Parameter(
    "year",
    openapi.IN_QUERY,
    description=(
        "desired year, enter 4 digits in the format 1XXX or 2XXX "
        "or you will receive 400 Bad request"
    ),
    type=openapi.TYPE_INTEGER,
)
ambassadors = openapi.Parameter(
    "ambassadors",
    openapi.IN_QUERY,
    description=(
        "ambassadors whose annual budget we want to see; enter the ambassador ID, "
        "you can enter several comma separated ambassador IDs"
    ),
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_INTEGER),
)


# TODO: add 4XX responses to Swagger api docs
class MerchApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for merch applications and annual merch budgets."""

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = MerchApplication.objects.all()
    serializer_class = MerchApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorOrReadOnly]
    filter_backends = [rf_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MerchApplicationsFilter
    ordering = ["pk"]

    def get_queryset(self):
        return MerchApplicationSerializer.setup_eager_loading(
            MerchApplication.objects.all()
        )

    def get_serializer_class(self):
        if self.action == "year_budget":
            return YearBudgetSerializer
        if self.action in ["create", "partial_update"]:
            return MerchApplicationCreateUpdateSerializer
        return MerchApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(
            tutor=self.request.user, application_number=generate_application_number()
        )

    @swagger_auto_schema(manual_parameters=[year, ambassadors])
    @action(methods=["get"], detail=False, filter_backends=[])
    def year_budget(self, request):
        """
        Shows the annual merch budget with detailed information
        by months and ambassadors.
        You need to pass the required year to the query parameters like this: ?year=2023
        Otherwise you will receive 400 Bad request.

        You can specify the IDs of particular ambassadors in the query parameters
        to view their annual budgets.
        You can specify several comma-separated ambassador IDs like this:
        ?year=2023&ambassadors=1,2
        """
        year_param = self.request.query_params.get("year", "")
        year = year_param if re.match(r"[1-2][0-9]{3}", year_param) else None
        ambassadors_ids = self.request.query_params.get("ambassadors")
        ambassadors = (
            Ambassador.objects.filter(id__in=ambassadors_ids.split(","))
            if ambassadors_ids
            else Ambassador.objects.all()
        )
        year_qs = (
            self.get_queryset().filter(created__year=year, ambassador__in=ambassadors)
            if ambassadors_ids
            else self.get_queryset().filter(created__year=year)
        )
        year_list = [application for application in year_qs]
        year_total = sum([application.merch_cost for application in year_list])
        if year_total == 0:
            return response.Response([], status=status.HTTP_200_OK)

        months = []
        for month in YEAR_MONTHS:
            month_list = [app for app in year_list if app.created.month == month[1]]
            month_total = sum([application.merch_cost for application in month_list])
            months.append({"month": month[0], "month_total": month_total})

        ambassadors_budgets = []
        for person in ambassadors:
            ambassador_list = [app for app in year_list if app.ambassador == person]
            ambassador_year_total = sum(
                [application.merch_cost for application in ambassador_list]
            )
            ambassador_months_budgets = []
            for month in YEAR_MONTHS:
                ambassador_month_list = [
                    app for app in ambassador_list if app.created.month == month[1]
                ]
                ambassador_month_total = sum(
                    [application.merch_cost for application in ambassador_month_list]
                )
                ambassador_months_budgets.append(
                    {"month": month[0], "month_total": ambassador_month_total}
                )

            ambassadors_budgets.append(
                {
                    "ambassador_name": person.name,
                    "ambassador_year_total": ambassador_year_total,
                    "ambassador_months_budgets": ambassador_months_budgets,
                }
            )

        payload = {
            "year": year,
            "year_total": year_total,
            "months": months,
            "ambassadors": ambassadors_budgets,
        }
        serializer = self.get_serializer_class()(
            data=payload,
            context={"request": request, "format": self.format_kwarg, "view": self},
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response.Response(serializer.data, status=status.HTTP_200_OK)

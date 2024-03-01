import re

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status, viewsets
from rest_framework.decorators import action

from .promo_serializers import MerchApplicationSerializer, YearBudgetSerializer
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


# TODO: выводит список заявок в странном порядке - не по id
# TODO: check all Swagger fields and responses, add 4XX responses
class MerchApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for merch applications and annual merch budgets."""

    # TODO: add http_method_names, permission_classes, filter_backends, filterset_class,
    # pagination_class and ordering options
    queryset = MerchApplication.objects.all()
    serializer_class = MerchApplicationSerializer

    def get_queryset(self):
        return MerchApplicationSerializer.setup_eager_loading(
            MerchApplication.objects.all()
        )

    def get_serializer_class(self):
        if self.action == "year_budget":
            return YearBudgetSerializer
        return MerchApplicationSerializer

    @swagger_auto_schema(manual_parameters=[year])
    @action(methods=["get"], detail=False)
    def year_budget(self, request):
        """
        Shows the annual merch budget with detailed information
        by months and ambassadors.
        You need to pass the required year to the parameters like this: ?year=2023
        Otherwise you will receive 400 Bad request.
        """
        year_param = self.request.query_params.get("year", "")
        year = year_param if re.match(r"[1-2][0-9]{3}", year_param) else None
        year_qs = self.get_queryset().filter(created__year=year)
        year_total = sum([application.merch_cost for application in year_qs])

        months = []
        for month in YEAR_MONTHS:
            month_qs = year_qs.filter(created__month=month[1])
            month_total = sum([application.merch_cost for application in month_qs])
            months.append({"month": month[0], "month_total": month_total})

        ambassadors = Ambassador.objects.all()
        ambassadors_budgets = []
        for person in ambassadors:
            ambassador_qs = year_qs.filter(ambassador=person)
            ambassador_year_total = sum(
                [application.merch_cost for application in ambassador_qs]
            )
            ambassador_months_budgets = []
            for month in YEAR_MONTHS:
                ambassador_month_qs = ambassador_qs.filter(created__month=month[1])
                ambassador_month_total = sum(
                    [application.merch_cost for application in ambassador_month_qs]
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
        serializer = self.get_serializer_class()(data=payload)
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response.Response(serializer.data, status=status.HTTP_200_OK)

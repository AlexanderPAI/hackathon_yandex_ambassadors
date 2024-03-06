import re

from django.utils.decorators import method_decorator
from django_filters import rest_framework as rf_filters
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse401Serializer,
    ErrorResponse403Serializer,
    ErrorResponse404Serializer,
    ValidationErrorResponseSerializer,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, response, status, viewsets
from rest_framework.decorators import action

from .filters import MerchApplicationsFilter, MerchFilter, PromocodeFilter
from .permissions import IsTutorOrReadOnly
from .promo_serializers import (
    MerchApplicationCreateUpdateSerializer,
    MerchApplicationSerializer,
    MerchCategorySerializer,
    MerchSerializer,
    PromocodeSerializer,
    YearBudgetSerializer,
)
from .utils import generate_application_number
from ambassadors.models import Ambassador
from promo.models import Merch, MerchApplication, MerchCategory, Promocode

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
    description=("desired year, enter 4 digits in the format 1XXX or 2XXX"),
    type=openapi.TYPE_INTEGER,
)
ambassadors = openapi.Parameter(
    "ambassadors",
    openapi.IN_QUERY,
    description=(
        "ambassadors whose annual budget we want to see; enter the ambassador ID, "
        "you can enter several comma-separated ambassador IDs"
    ),
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_INTEGER),
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Get all merch applications",
        responses={
            200: MerchApplicationSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
        manual_parameters=[
            openapi.Parameter(
                "application_number",
                openapi.IN_QUERY,
                description="filtering by partial occurrence in application_number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ambassador",
                openapi.IN_QUERY,
                description="filtering by ambassador ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "tutor",
                openapi.IN_QUERY,
                description="filtering by tutor (curator) ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description=(
                    "filtering by merch application creation date, "
                    "input examples: '2020-01-01', '2024-03-04T16:20:55'"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description=(
                    "filtering by merch application creation date, "
                    "input examples: '2020-01-01', '2024-03-04T16:20:55'"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "merch",
                openapi.IN_QUERY,
                description=(
                    "filtering by merch slug, accepts several comma-separated "
                    "values, for example: ?merch=coffee-l,shopper-gray"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_SLUG,
            ),
        ],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Get merch application by id",
        responses={
            200: MerchApplicationSerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create merch application",
        responses={
            201: MerchApplicationCreateUpdateSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Edit merch application",
        responses={
            200: MerchApplicationCreateUpdateSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
            403: ErrorResponse403Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Delete merch application",
        responses={
            204: "",
            401: ErrorResponse401Serializer,
            403: ErrorResponse403Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="budget_info",
    decorator=swagger_auto_schema(
        operation_summary="Show the annual merch budget",
        responses={200: YearBudgetSerializer, 401: ErrorResponse401Serializer},
        manual_parameters=[year, ambassadors],
    ),
)
class MerchApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for merch applications and annual merch budgets.
    By default, sorting is done by ID.
    You can also sort them by the following fields: ambassador__name,
    ambassador__clothing_size, ambassador__shoe_size, ambassador__address__postal_code,
    application_number, merch__name, 'tutor__first_name,tutor__last_name' (combined
    curator's first and last names), created. Example: ?ordering=ambassador__name
    (in the end of URL).
    For reverse sorting insert a minus sign before the field name
    like this: ?ordering=-ambassador__name (in the end of URL).

    You can filter merch appications by application_number (by partial occurrence in
    a string), ambassador (by ID), tutor (by ID), merch (by slug, can accept sevelal
    comma-separated slugs), start_date and end_date (takes datetime string, examples:
    "2020-01-01", "2024-03-04T16:20:55").
    """

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = MerchApplication.objects.all()
    serializer_class = MerchApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorOrReadOnly]
    filter_backends = [rf_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MerchApplicationsFilter
    ordering_fields = [
        "ambassador__name",
        "ambassador__clothing_size",
        "ambassador__shoe_size",
        "ambassador__address__postal_code",
        "application_number",
        "merch__name",
        "tutor__first_name",
        "tutor__last_name",
        "created",
    ]
    ordering = ["pk"]

    def get_queryset(self):
        return MerchApplicationSerializer.setup_eager_loading(
            MerchApplication.objects.all()
        )

    def get_serializer_class(self):
        if self.action == "budget_info":
            return YearBudgetSerializer
        if self.action in ["create", "partial_update"]:
            return MerchApplicationCreateUpdateSerializer
        return MerchApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(
            tutor=self.request.user, application_number=generate_application_number()
        )

    @action(methods=["get"], detail=False, filter_backends=[])
    def budget_info(self, request):
        """
        Shows the annual merch budget with detailed information
        by months and ambassadors.
        You need to pass the required year to the query parameters like this: ?year=2023

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


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Get all merch categories",
        responses={200: MerchCategorySerializer, 401: ErrorResponse401Serializer},
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Get merch category by id",
        responses={
            200: MerchCategorySerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create merch category",
        responses={
            201: MerchCategorySerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Edit merch category",
        responses={
            200: MerchCategorySerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Delete merch category",
        responses={
            204: "",
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
class MerchCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for categories of merch."""

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = MerchCategory.objects.all()
    serializer_class = MerchCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Get all merch species",
        responses={
            200: MerchSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
        manual_parameters=[
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="filtering by partial occurrence in name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "size",
                openapi.IN_QUERY,
                description=(
                    "filtering by size (exact match), accepts several comma-separated "
                    "values, for example: ?size=L,M"
                ),
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description=(
                    "filtering by category slug, accepts several comma-separated "
                    "values, for example: ?category=socks,shopper"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_SLUG,
            ),
            openapi.Parameter(
                "min_cost",
                openapi.IN_QUERY,
                description="filtering by merch cost, including the entered value",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "max_cost",
                openapi.IN_QUERY,
                description="filtering by merch cost, including the entered value",
                type=openapi.TYPE_NUMBER,
            ),
        ],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Get merch by id",
        responses={
            200: MerchSerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create merch",
        responses={
            201: MerchSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Edit merch",
        responses={
            200: MerchSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Delete merch",
        responses={
            204: "",
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
class MerchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for merch species.
    Basic items sorting is carried out by ID.
    You can sort objects by other fields (by name, size, slug, cost, and category id)
    like this: ?ordering=cost (in the end of URL).
    For reverse sorting insert a minus sign before the field name
    like this: ?ordering=-cost (in the end of URL).
    """

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Merch.objects.all()
    serializer_class = MerchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [rf_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MerchFilter
    ordering = ["pk"]

    def get_queryset(self):
        return MerchSerializer.setup_eager_loading(Merch.objects.all())


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Get all promocodes",
        responses={
            200: PromocodeSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
        manual_parameters=[
            openapi.Parameter(
                "ambassador_name",
                openapi.IN_QUERY,
                description="filtering by partial occurrence in ambassador name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ambassador_status",
                openapi.IN_QUERY,
                description=(
                    "filtering by ambassador status slug, accepts several "
                    "comma-separated values, for example: "
                    "?ambassador_status=active,paused"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_SLUG,
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description=(
                    "filtering by promocode creation date, "
                    "input examples: '2020-01-01', '2024-03-04T16:20:55'"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description=(
                    "filtering by promocode creation date, "
                    "input examples: '2020-01-01', '2024-03-04T16:20:55'"
                ),
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
        ],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Get promocode by id",
        responses={
            200: PromocodeSerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create promocode",
        responses={
            201: PromocodeSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Edit promocode",
        responses={
            200: PromocodeSerializer,
            400: ValidationErrorResponseSerializer,
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Delete promocode",
        responses={
            204: "",
            401: ErrorResponse401Serializer,
            404: ErrorResponse404Serializer,
        },
    ),
)
class PromocodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for promocodes.
    By default, sorting is done by ID.
    You can also sort promocodes by the following fields: code, created,
    ambassador__name, ambassador__status, ambassador__telegram_id.
    Example: ?ordering=ambassador__name (in the end of URL).
    For reverse sorting insert a minus sign before the field name
    like this: ?ordering=-ambassador__name (in the end of URL).
    """

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [rf_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PromocodeFilter
    ordering_fields = [
        "code",
        "created",
        "ambassador__name",
        "ambassador__status",
        "ambassador__telegram_id",
    ]
    ordering = ["pk"]

    def get_queryset(self):
        return PromocodeSerializer.setup_eager_loading(Promocode.objects.all())

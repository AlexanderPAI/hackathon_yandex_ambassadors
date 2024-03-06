from django.db.models import BooleanField, ExpressionWrapper, Q
from django_filters import rest_framework as rf_filters

from promo.models import Merch, MerchApplication, Promocode


class CharFilterInFilter(rf_filters.BaseInFilter, rf_filters.CharFilter):
    """Custom char filter allowing comma-separated incoming values."""

    pass


# TODO: drf-yasg mistakenly considers the types of all fields to be strings
class MerchApplicationsFilter(rf_filters.FilterSet):
    """
    Class for filtering merch applications.

    The filter for the 'application_number' field works on a partial occurrence
    (istartswith and icontains).

    Filters for fields 'ambassador', 'tutor' work by ID.
    The filter for the 'merch' field works by slug and accepts several comma-separated
    values, for example: ?merch=coffee-l,shopper-gray (in the end of URL).

    Filters 'start_date' and 'end_date' take datetime string
    (input examples: "2020-01-01", "2024-03-04T16:20:55") as input and compare it
    to the value of the 'created' field of each merch application.
    """

    application_number = rf_filters.CharFilter(
        method="startswith_contains_union_method"
    )
    start_date = rf_filters.DateTimeFilter(field_name="created", lookup_expr="gte")
    end_date = rf_filters.DateTimeFilter(field_name="created", lookup_expr="lte")
    merch = CharFilterInFilter(field_name="merch__slug")

    class Meta:
        model = MerchApplication
        fields = [
            "application_number",
            "ambassador",
            "tutor",
            "start_date",  # example: "2024-01-01"
            "end_date",  # example: "2024-01-01"
            "merch",
        ]

    def startswith_contains_union_method(self, queryset, name, value):
        """
        When using sqlite DB, filtering will be case-sensitive;
        when using PostgreSQL DB, filtering will be case-insensitive as it should be.
        """
        if not bool(value):
            return queryset
        return (
            queryset.filter(
                Q(application_number__istartswith=value)
                | Q(application_number__icontains=value)
            )
            .annotate(
                is_start=ExpressionWrapper(
                    Q(application_number__istartswith=value),
                    output_field=BooleanField(),
                )
            )
            .order_by("-is_start")
        )


# TODO: drf-yasg mistakenly considers the types of all fields to be strings
class PromocodeFilter(rf_filters.FilterSet):
    """
    Class for filtering promocodes.

    The filter for the 'ambassador_name' works on a partial occurrence
    (istartswith and icontains).

    The filter for the 'ambassador_status' works by slug and accepts several
    comma-separated values, for example: ?ambassador_status=active,paused (in the end
    of URL).

    Filters 'start_date' and 'end_date' take datetime string
    (input examples: "2020-01-01", "2024-03-04T16:20:55") as input and compare it
    to the value of the 'created' field of each merch application.
    """

    ambassador_name = rf_filters.CharFilter(
        field_name="ambassador__name", method="startswith_contains_union_method"
    )
    ambassador_status = CharFilterInFilter(field_name="ambassador__status__slug")
    start_date = rf_filters.DateTimeFilter(field_name="created", lookup_expr="gte")
    end_date = rf_filters.DateTimeFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = Promocode
        fields = ["ambassador_name", "ambassador_status", "start_date", "end_date"]

    def startswith_contains_union_method(self, queryset, name, value):
        """
        When using sqlite DB, filtering will be case-sensitive;
        when using PostgreSQL DB, filtering will be case-insensitive as it should be.
        """
        if not bool(value):
            return queryset
        return (
            queryset.filter(
                Q(ambassador__name__istartswith=value)
                | Q(ambassador__name__icontains=value)
            )
            .annotate(
                is_start=ExpressionWrapper(
                    Q(ambassador__name__istartswith=value),
                    output_field=BooleanField(),
                )
            )
            .order_by("-is_start")
        )


# TODO: drf-yasg mistakenly considers the types of all fields to be strings
class MerchFilter(rf_filters.FilterSet):
    """
    Class for filtering merch species.

    The filter for the 'name' works on a partial occurrence (istartswith and icontains).

    The filter for the 'size' works by exact match and accepts several comma-separated
    values, for example: ?size=L,M (in the end of URL).

    The filter for the 'category' works by slug and accepts several comma-separated
    values, for example: ?category=socks,shopper (in the end of URL).

    Filters 'min_cost' and 'max_cost' take integer or float number as input and compare
    it to the value of the 'cost' field of each merch item. The results include
    the entered value.
    """

    name = rf_filters.CharFilter(method="startswith_contains_union_method")
    size = CharFilterInFilter()
    category = CharFilterInFilter(field_name="category__slug")
    min_cost = rf_filters.NumberFilter(method="get_min_cost")
    max_cost = rf_filters.NumberFilter(method="get_max_cost")

    class Meta:
        model = Merch
        fields = ["name", "size", "category", "min_cost", "max_cost"]

    def startswith_contains_union_method(self, queryset, name, value):
        """
        When using sqlite DB, filtering will be case-sensitive;
        when using PostgreSQL DB, filtering will be case-insensitive as it should be.
        """
        if not bool(value):
            return queryset
        return (
            queryset.filter(Q(name__istartswith=value) | Q(name__icontains=value))
            .annotate(
                is_start=ExpressionWrapper(
                    Q(name__istartswith=value),
                    output_field=BooleanField(),
                )
            )
            .order_by("-is_start")
        )

    def get_min_cost(self, queryset, name, value):
        if value <= 0:
            return queryset
        merch_ids = [obj.pk for obj in queryset if obj.cost >= value]
        if merch_ids:
            return queryset.filter(pk__in=merch_ids)
        return queryset.none()

    def get_max_cost(self, queryset, name, value):
        if value <= 0:
            return queryset
        merch_ids = [obj.pk for obj in queryset if obj.cost <= value]
        if merch_ids:
            return queryset.filter(pk__in=merch_ids)
        return queryset.none()

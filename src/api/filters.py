from django.db.models import BooleanField, ExpressionWrapper, Q
from django_filters import rest_framework as rf_filters

from promo.models import MerchApplication


class CharFilterInFilter(rf_filters.BaseInFilter, rf_filters.CharFilter):
    """Custom char filter allowing comma-separated incoming values."""

    pass


# TODO: drf-yasg mistakenly considers the types of all fields to be strings
class MerchApplicationsFilter(rf_filters.FilterSet):
    """
    Class for filtering merch applications.

    The filter for the 'application_number' field works on a partial occurrence
    (istartswith and icontains).

    Filters for fields 'ambassador', 'tutor' and 'merch' work by ID.
    The filter for the 'merch' field can accept several merch IDs separated by commas.

    Filters 'start_date' and 'end_date' take datetime string
    (input examples: "2020-01-01", "2024-03-04T16:20:55") as input and compare it
    with the value of the 'created' field of each merch application.
    """

    application_number = rf_filters.CharFilter(
        method="startswith_contains_union_method"
    )
    start_date = rf_filters.DateTimeFilter(field_name="created", lookup_expr="gte")
    end_date = rf_filters.DateTimeFilter(field_name="created", lookup_expr="lte")
    merch = CharFilterInFilter()  # TODO: filter merch by slug, change docstring

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

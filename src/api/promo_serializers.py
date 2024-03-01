from django.db.models import F, Prefetch, Sum
from rest_framework import serializers

from promo.models import MerchApplication, MerchInApplication


class MerchApplicationSerializer(serializers.ModelSerializer):
    """Serializer for merch applications."""

    class Meta:
        model = MerchApplication
        fields = "__all__"

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Performs necessary eager loading of merch applications data."""
        return queryset.prefetch_related(
            Prefetch(
                "merch_in_applications",
                queryset=MerchInApplication.objects.select_related("merch"),
            )
        ).annotate(
            merch_cost=Sum(
                F("merch_in_applications__quantity")
                * F("merch_in_applications__merch__cost"),
                default=0,
            ),
        )


class MonthBudgetSerializer(serializers.Serializer):
    """Serializer to display merch budget for months of the year."""

    month = serializers.CharField()
    month_total = serializers.FloatField()


class AmbassadorBudgetSerializer(serializers.Serializer):
    """Serializer to display merch budget for individual ambassadors."""

    ambassador_name = serializers.CharField()
    ambassador_year_total = serializers.FloatField()
    ambassador_months_budgets = MonthBudgetSerializer(many=True)


class YearBudgetSerializer(serializers.Serializer):
    """Serializer to display annual merch budget."""

    year = serializers.IntegerField()
    year_total = serializers.FloatField()
    months = MonthBudgetSerializer(many=True)
    ambassadors = AmbassadorBudgetSerializer(many=True)
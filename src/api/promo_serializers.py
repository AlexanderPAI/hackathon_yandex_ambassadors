from collections import OrderedDict

from django.db import transaction
from django.db.models import F, Prefetch, Sum
from rest_framework import serializers

from ambassadors.models import Address, Ambassador, Status
from promo.models import (
    Merch,
    MerchApplication,
    MerchCategory,
    MerchInApplication,
    Promocode,
)
from users.models import User


class AddressMerchSerializer(serializers.ModelSerializer):
    """Serializer to display ambassador address in merch applications."""

    class Meta:
        model = Address
        fields = "__all__"


class AmbassadorMerchSerializer(serializers.ModelSerializer):
    """Serializer to display ambassador details in merch applications."""

    address = AddressMerchSerializer()

    class Meta:
        model = Ambassador
        fields = ["id", "name", "clothing_size", "shoe_size", "address"]


class TutorMerchSerializer(serializers.ModelSerializer):
    """Serializer to display tutor name in merch applications."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name"]

    def get_full_name(self, obj) -> str:
        """Shows tutor full name."""
        return str(obj)


class StatusPromocodeSerializer(serializers.ModelSerializer):
    """Serializer to display ambassador status in promocodes serializer."""

    class Meta:
        model = Status
        fields = ["id", "name", "slug"]


class AmbassadorPromocodeSerializer(serializers.ModelSerializer):
    """Serializer to display ambassador details in promocodes serializer."""

    telegram = serializers.CharField(source="telegram_id")
    status = StatusPromocodeSerializer()

    class Meta:
        model = Ambassador
        fields = ["id", "name", "status", "created", "telegram"]


class MerchInApplicationSerializer(serializers.ModelSerializer):
    """Serializer to display info on merch in an application."""

    id = serializers.IntegerField(source="merch.id", read_only=True)
    name = serializers.ReadOnlyField(source="merch.name")
    category = serializers.ReadOnlyField(source="merch.category.name")
    slug = serializers.SlugField(source="merch.slug", read_only=True)
    size = serializers.ReadOnlyField(source="merch.size")
    cost = serializers.FloatField(source="merch.cost", read_only=True)
    name_and_size = serializers.SerializerMethodField()

    class Meta:
        model = MerchInApplication
        fields = (
            "id",
            "name",
            "size",
            "name_and_size",
            "category",
            "slug",
            "cost",
            "quantity",
        )

    def get_name_and_size(self, obj) -> str:
        """Shows name and size combination."""
        return str(obj.merch)


class MerchInApplicationCreateUpdateSerializer(MerchInApplicationSerializer):
    """Serializer to create/edit merch in an application."""

    id = serializers.PrimaryKeyRelatedField(
        source="merch.id", queryset=Merch.objects.all()
    )

    class Meta(MerchInApplicationSerializer.Meta):
        fields = ("id", "quantity")

    def to_representation(self, instance):
        old_repr = super().to_representation(instance)
        new_repr = OrderedDict()
        new_repr["id"] = old_repr["id"]
        new_repr["name"] = instance.merch.name
        new_repr["category"] = instance.merch.category.name
        new_repr["slug"] = instance.merch.slug
        new_repr["size"] = instance.merch.size
        new_repr["cost"] = instance.merch.cost
        new_repr["quantity"] = old_repr["quantity"]
        return new_repr


class MerchApplicationSerializer(serializers.ModelSerializer):
    """Serializer to display merch applications."""

    application_number = serializers.ReadOnlyField()
    ambassador = AmbassadorMerchSerializer()
    tutor = TutorMerchSerializer()
    merch = MerchInApplicationSerializer(many=True, source="merch_in_applications")
    merch_cost = serializers.SerializerMethodField()

    class Meta:
        model = MerchApplication
        fields = (
            "id",
            "application_number",
            "ambassador",
            "tutor",
            "created",
            "merch_cost",
            "merch",
        )

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Performs necessary eager loading of merch applications data."""
        return (
            queryset.select_related("ambassador__address", "tutor")
            .prefetch_related(
                Prefetch(
                    "merch_in_applications",
                    queryset=MerchInApplication.objects.select_related(
                        "merch__category"
                    ),
                )
            )
            .annotate(
                merch_cost=Sum(
                    F("merch_in_applications__quantity")
                    * F("merch_in_applications__merch__cost"),
                    default=0,
                ),
            )
        )

    def get_merch_cost(self, obj) -> float:
        """Shows the total cost of the merch in the application (annotated field)."""
        return obj.merch_cost


# TODO: drf-yasg shows incorrect merch field in response body - without taking into
# account the MerchInApplicationCreateUpdateSerializer.to_representation method
class MerchApplicationCreateUpdateSerializer(MerchApplicationSerializer):
    """Serializer to create/edit merch applications."""

    application_number = serializers.CharField(required=False)
    tutor = serializers.PrimaryKeyRelatedField(read_only=True)
    merch = MerchInApplicationCreateUpdateSerializer(
        many=True, source="merch_in_applications"
    )
    merch_cost = serializers.SerializerMethodField()

    def get_merch_cost(self, obj) -> float:
        """Calculates the total cost of the merch in the application."""
        return sum(
            [
                item.quantity * item.merch.cost
                for item in obj.merch_in_applications.all()
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        """Creates an application for merch taking into account m2m connections."""
        merch = validated_data.pop("merch_in_applications")
        application = MerchApplication.objects.create(**validated_data)
        for item in merch:
            MerchInApplication.objects.create(
                application=application,
                merch=item["merch"]["id"],
                quantity=item["quantity"],
            )
        return application

    @transaction.atomic
    def update(self, instance, validated_data):
        """Updates some fields in merch application during PATCH-requests."""
        if validated_data.get("merch_in_applications") is not None:
            merch = validated_data.pop("merch_in_applications")
            instance.merch.clear()
            for item in merch:
                MerchInApplication.objects.create(
                    application=instance,
                    merch=item["merch"]["id"],
                    quantity=item["quantity"],
                )
        super().update(instance, validated_data)
        return instance


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


class MerchCategorySerializer(serializers.ModelSerializer):
    """Serializer for categories of merch."""

    class Meta:
        model = MerchCategory
        fields = ["id", "name", "slug"]


class MerchSerializer(serializers.ModelSerializer):
    """Serializer for merch species."""

    category = MerchCategorySerializer()

    class Meta:
        model = Merch
        fields = ["id", "name", "size", "slug", "cost", "category"]

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Performs necessary eager loading of merch species data."""
        return queryset.select_related("category")


class PromocodeSerializer(serializers.ModelSerializer):
    """Serializer for promocodes."""

    ambassador = AmbassadorPromocodeSerializer()

    class Meta:
        model = Promocode
        fields = ["id", "code", "created", "is_active", "ambassador"]

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Performs necessary eager loading of merch species data."""
        return queryset.select_related("ambassador__status")

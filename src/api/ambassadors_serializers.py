from rest_framework import serializers

from ambassadors.models import (
    Activity,
    Address,
    Ambassador,
    AmbassadorActivity,
    Program,
    Purpose,
)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "postal_code",
            "country",
            "city",
            "street",
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("name",)


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ("name",)


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = ("name", "personal_purpose")


class AmbassadorReadSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True, many=True)
    address = AddressSerializer(read_only=True)
    purpose = serializers.StringRelatedField(read_only=True)
    program = serializers.StringRelatedField(read_only=True)
    tutor = serializers.StringRelatedField(read_only=True)
    status = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "pk",
            "created",
            "name",
            "gender",
            "clothing_size",
            "shoe_size",
            "education",
            "job",
            "email",
            "phone_number",
            "telegram_id",
            "whatsapp",
            "activity",
            "blog_link",
            "onboarding_status",
            "purpose",
            "about_me",
            "tutor",
            "status",
            "program",
            "address",
            "promocodes",
        )

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Performs necessary eager loading of ambassadors data."""
        return queryset.select_related(
            "tutor", "address", "status", "program", "purpose"
        ).prefetch_related("activity", "promocodes")


class AmbassadorCreateSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(many=True)
    address = AddressSerializer(required=False)
    purpose = PurposeSerializer()
    program = ProgramSerializer()

    class Meta:
        model = Ambassador
        fields = (
            "name",
            "gender",
            "clothing_size",
            "shoe_size",
            "education",
            "job",
            "email",
            "phone_number",
            "telegram_id",
            "activity",
            "blog_link",
            "purpose",
            "about_me",
            "program",
            "address",
        )

    def create(self, validated_data):
        program_data = validated_data.pop("program")
        purpose_data = validated_data.pop("purpose")
        activities = validated_data.pop("activity")
        address = Address.objects.create(**validated_data.pop("address"))
        ambassador_program = Program.objects.get_or_create(**program_data)[0]
        ambassador_purpose = Purpose.objects.get_or_create(**purpose_data)[0]
        validated_data["program"] = ambassador_program
        validated_data["purpose"] = ambassador_purpose

        ambassador = Ambassador.objects.create(**validated_data, address=address)

        for activity in activities:
            activity = Activity.objects.get_or_create(**activity)[0]
            AmbassadorActivity(ambassador=ambassador, activity=activity).save()
        return ambassador

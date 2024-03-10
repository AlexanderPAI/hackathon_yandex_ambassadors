from rest_framework import serializers

from ambassadors.models import (
    Activity,
    Address,
    Ambassador,
    AmbassadorPurpose,
    AmbassadorActivity,
    Program,
    Purpose,
    Status,
)


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model."""

    class Meta:
        model = Address
        fields = (
            "id",
            "postal_code",
            "country",
            "city",
            "street",
        )


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""

    class Meta:
        model = Activity
        fields = ("id", "name",)


class ProgramSerializer(serializers.ModelSerializer):
    """Serializer for Program model"""

    class Meta:
        model = Program
        fields = ("id", "name",)


class PurposeSerializer(serializers.ModelSerializer):
    """Serializer for Purpose model"""

    class Meta:
        model = Purpose
        fields = ("id", "name")


class AmbassadorPurposeSerializer(serializers.ModelSerializer):
    """Serializer for AmbassadorPurpose model"""

    id = serializers.ReadOnlyField(source='purpose.id')
    name = serializers.CharField(source='purpose.name')
    personal_purpose = serializers.CharField(source='purpose.personal_purpose')

    class Meta:
        model = AmbassadorPurpose
        fields = ("id", "name", "personal_purpose",)


class AmbassadorPurposeCreateSerializer(serializers.ModelSerializer):
    """Serializer for create AmbassadorPurpose model."""

    id = serializers.PrimaryKeyRelatedField(
        source='purpose',
        queryset=Purpose.objects.all()
    )

    personal_purpose = serializers.CharField()

    class Meta:
        model = AmbassadorPurpose
        fields = ("id", "personal_purpose",)


class AmbassadorReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Ambassador model"""
    activity = ActivitySerializer(read_only=True, many=True)
    address = AddressSerializer(read_only=True)
    purpose = PurposeSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    tutor = serializers.StringRelatedField(read_only=True)
    status = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "id",
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
    """Serializer for creating Ambassador model"""
    activity = ActivitySerializer(many=True)
    purpose = PurposeSerializer()
    address = AddressSerializer()
    # program = ProgramSerializer()

    # purpose = PurposeSerializer()
    # program = ProgramSerializer()

    program = serializers.SlugRelatedField(slug_field="name", read_only=True)

    # status = serializers.SlugRelatedField(slug_field="slug", read_only=True)

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
            "status",
        )

    def create(self, validated_data):
        print(self.initial_data)
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(validated_data)
        print("-------------------------------------------")
        print("-------------------------------------------")
        print("-------------------------------------------")
        print("-------------------------------------------")
        print("-------------------------------------------")
        print("-------------------------------------------")
        # program = Program.objects.get_or_create(name=program_data["name"])
        activities = validated_data.pop("activity")
        address = Address.objects.create(**validated_data.pop("address"))
        # ambassador_program = Program.objects.get_or_create(**program_data)[0]
        # ambassador_purpose = Purpose.objects.get_or_create(**purpose_data)[0]
        # validated_data["program"] = ambassador_program
        # validated_data["purpose"] = ambassador_purpose
        purpose, status = Purpose.objects.get_or_create(**validated_data.pop("purpose"))
        ambassador = Ambassador.objects.create(**validated_data, address=address)

        AmbassadorPurpose(ambassador=ambassador, purpose=purpose).save()

        for activity in activities:
            activity = Activity.objects.get_or_create(**activity)[0]
            AmbassadorActivity(ambassador=ambassador, activity=activity).save()
        return ambassador

    def update(self, instance, validated_data):
        instance.name = validated_data.pop("name", instance.name)
        instance.gender = validated_data.pop("gender", instance.gender)
        instance.clothing_size = validated_data.pop(
            "clothing_size", instance.clothing_size
        )
        instance.shoe_size = validated_data.pop("shoe_size", instance.shoe_size)
        instance.education = validated_data.pop("education", instance.education)
        instance.job = validated_data.pop("job", instance.job)
        instance.email = validated_data.pop("email", instance.email)
        instance.phone_number = validated_data.pop(
            "phone_number", instance.phone_number
        )
        instance.telegram_id = validated_data.pop(
            "telegram_id", instance.telegram_id
        )
        instance.whatsapp = validated_data.pop("whatsapp", instance.whatsapp)
        instance.blog_link = validated_data.pop("blog_link", instance.blog_link)
        instance.onboarding_status = validated_data.pop(
            "onboarding_status", instance.onboarding_status
        )
        instance.about_me = validated_data.pop("about_me", instance.about_me)

        instance.status = validated_data.pop("status", instance.status)
        instance.program = validated_data.pop("program", instance.program)
        instance.address = validated_data.pop("address", instance.address)
        instance.purpose = validated_data.pop("purpose", instance.purpose)
        instance.tutor = validated_data.pop("tutor", instance.tutor)

        if "activity" in validated_data:
            AmbassadorActivity.objects.filter(ambassador=instance).all().delete()
            for activity in validated_data["activity"]:
                activity, status = Activity.objects.get_or_create(name=activity["name"])
                AmbassadorActivity(
                    ambassador=instance,
                    activity=activity
                ).save()
        instance.save()
        return instance

    def to_representation(self, instance):
        return AmbassadorReadSerializer(instance, context=self.context).data

# class AmbassadorUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ambassador
#         fields = (
#             "name",
#             "gender",
#             "clothing_size",
#             "shoe_size",
#             "education",
#             "job",
#             "email",
#             "phone_number",
#             "telegram_id",
#             "activity",
#             "blog_link",
#             "purpose",
#             "about_me",
#             "program",
#             "address",
#             "status",
#         )

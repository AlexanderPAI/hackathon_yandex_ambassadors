from rest_framework.serializers import (  # StringRelatedField,
    ModelSerializer,
    ReadOnlyField,
)

from content.models import Guide, GuideKit, GuideTask, GuideTaskGuideKit

# Content,; ContentPlatform,; GuideStatus,; MerchPhoto,; Review,; ReviewPlatfrom,


class GuideTaskSerializer(ModelSerializer):

    class Meta:
        model = GuideTask
        fields = "__all__"


class GuideTaskGuideKitSerializer(ModelSerializer):
    id = ReadOnlyField(source="guide_task.id")
    type = ReadOnlyField(source="guide_task.type")

    class Meta:
        model = GuideTaskGuideKit
        fields = (
            "id",
            "type",
        )


class GuideKitSerializer(ModelSerializer):
    tasks = GuideTaskGuideKitSerializer(many=True)

    class Meta:
        model = GuideKit
        fields = (
            "name",
            "tasks",
        )


# class GuideKitSerializer(ModelSerializer):

#     class Meta:
#         model = GuideKit
#         fields = "__all__"


class GuideSerializer(ModelSerializer):

    class Meta:
        model = Guide
        fields = "__all__"

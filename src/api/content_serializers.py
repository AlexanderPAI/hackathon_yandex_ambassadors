import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from ambassadors.models import Ambassador
from content.models import (
    Content,
    Guide,
    GuideKit,
    GuideTask,
    GuideTaskGuideKit,
    MerchPhoto,
)


def get_platfrom(link):
    platform = link[:]
    if "//" in platform:
        platform = platform.split("//")[1].split("/")
        if "www." in platform[0]:
            platform[0] = platform[0].replace("www.", "")
        if "yandex" in platform[0] or "google" in platform[0]:
            return platform[0] + "/" + platform[1]
        return platform[0]
    return platform.split("/")[0]


def get_type(platform):
    reviews_platforms = [
        "career.habr.com",
        "sravni.ru",
        "tutortop.ru",
        "irecommend.ru",
        "journal.tinkoff.ru",
        "mooc.ru",
        "katalog-kursov.ru",
        "otzovik.com",
        "yandex.ru/maps/",
        "google.com/maps",
    ]
    if platform in reviews_platforms:
        return "review"
    return "content"


class GuideTaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи для гайда."""

    class Meta:
        model = GuideTask
        fields = "__all__"


class GuideTaskGuideKitSerializer(serializers.ModelSerializer):
    """
    Всмпомогательный сериализатор для переопределения
    полей id и type.
    """

    id = serializers.ReadOnlyField(source="task.id")
    type = serializers.ReadOnlyField(source="task.type")

    class Meta:
        model = GuideTaskGuideKit
        fields = (
            "id",
            "type",
        )


class GuideKitSerializer(serializers.ModelSerializer):
    """Сериализатор набора задач для гайда."""

    tasks = GuideTaskSerializer(many=True)

    class Meta:
        model = GuideKit
        fields = "__all__"


class GuideTaskGuideKitCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания вспомогательной модели."""

    id = serializers.PrimaryKeyRelatedField(
        source="task.id", queryset=GuideTask.objects.all()
    )
    type = serializers.ReadOnlyField(source="task.type")

    class Meta:
        model = GuideTaskGuideKit
        fields = ("id", "type")


class GuideKitCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления набора задач."""

    tasks = GuideTaskGuideKitCreateSerializer(many=True, source="connected_tasks")

    class Meta:
        model = GuideKit
        fields = (
            "id",
            "name",
            "tasks",
        )

    def create(self, validated_data):
        tasks = validated_data.pop("connected_tasks")
        instance = super().create(validated_data)
        GuideTaskGuideKit.objects.bulk_create(
            GuideTaskGuideKit(
                guide_kit=instance,
                task=data["task"]["id"],
            )
            for data in tasks
        )
        return instance

    def update(self, instance, validated_data):
        tasks = validated_data.pop("connected_tasks")
        GuideTaskGuideKit.objects.filter(guide_kit=instance.id).delete()
        for data in tasks:
            GuideTaskGuideKit(
                guide_kit=instance,
                task=data["task"]["id"],
            ).save()
        return super().update(instance, validated_data)


class GuideSerializer(serializers.ModelSerializer):
    """Сериализатор гайда."""

    guide_kit = serializers.StringRelatedField()
    tasks = GuideTaskSerializer(many=True, source="guide_kit.tasks", required=False)
    status = serializers.ChoiceField(
        choices=Guide.STATUS,
    )

    class Meta:
        model = Guide
        fields = "__all__"


class GuideCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/обновления гайда."""

    class Meta:
        model = Guide
        fields = "__all__"


class Base64ImageField(serializers.ImageField):
    """Сериазитор для декодирования изображения."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class MerchPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор для Фото в мерче."""

    photo = Base64ImageField()

    class Meta:
        model = MerchPhoto
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    """Сериализтор контента."""

    image = Base64ImageField()

    class Meta:
        model = Content
        fields = (
            "id",
            "created",
            "link",
            "is_guide_content",
            "ambassador",
            "platform",
            "type",
            "image",
        )


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания контента."""

    image = Base64ImageField()

    class Meta:
        model = Content
        fields = (
            "id",
            "created",
            "link",
            "is_guide_content",
            "ambassador",
            "platform",
            "type",
            "image",
        )

    def create(self, validated_data):
        link = validated_data["link"]
        platform = get_platfrom(link)
        type = get_type(platform)
        return Content.objects.create(
            **validated_data,
            platform=platform,
            type=type,
        )


class ContentPageSerialzier(serializers.ModelSerializer):
    """Сериализатор для страницы Контент."""

    review = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = (
            "name",
            "telegram_id",
            "review",
            "content",
        )

    def get_review(self, obj):
        review = obj.content.filter(type="review")
        if review:
            return review[0].link
        return "Еще нет отзывов"

    def get_content(self, obj):
        content = obj.content.filter(type="content")
        if content:
            return content[0].link
        return "Еще нет контента"

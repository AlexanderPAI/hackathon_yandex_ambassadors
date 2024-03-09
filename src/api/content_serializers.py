from rest_framework import serializers

from content.models import Guide, GuideKit, GuideStatus, GuideTask, GuideTaskGuideKit


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


class GuideStatusSerializer(serializers.ModelSerializer):
    """Сериализатор статуса гайда."""

    class Meta:
        model = GuideStatus
        fields = "__all__"


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

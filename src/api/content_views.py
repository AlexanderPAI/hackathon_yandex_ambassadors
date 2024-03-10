from rest_framework.viewsets import ModelViewSet

from api.content_serializers import (
    GuideCreateUpdateSerializer,
    GuideKitCreateUpdateSerializer,
    GuideKitSerializer,
    GuideSerializer,
    GuideStatusSerializer,
    GuideTaskSerializer,
)
from content.models import Guide, GuideKit, GuideStatus, GuideTask


# TODO: duplicate queries in guide kits
class GuideTaskViewSet(ModelViewSet):
    """Представление задачи для гайда."""

    queryset = GuideTask.objects.all()
    serializer_class = GuideTaskSerializer


class GuideKitViewSet(ModelViewSet):
    """Представление набора задач для гайда."""

    queryset = GuideKit.objects.all()
    serializer_class = GuideKitSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return GuideKitCreateUpdateSerializer
        return GuideKitSerializer


# TODO: duplicate queries guide status?
class GuideStatusViewSet(ModelViewSet):
    """Представление статуса гайда."""

    queryset = GuideStatus.objects.all()
    serializer_class = GuideStatusSerializer


# TODO: duplicate queries guides?
class GuideViewSet(ModelViewSet):
    """Представление гайда."""

    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return GuideCreateUpdateSerializer
        return GuideSerializer

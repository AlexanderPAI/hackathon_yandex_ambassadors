from rest_framework.viewsets import ModelViewSet

from api.content_serializers import GuideSerializer, GuideCreateUpdateSerializer, GuideStatusSerializer, GuideKitSerializer, GuideTaskSerializer, GuideKitCreateUpdateSerializer
from content.models import Guide, GuideKit, GuideStatus, GuideTask


class GuideTaskViewSet(ModelViewSet):
    """Представление задачи для гайда."""
    queryset = GuideTask.objects.all()
    serializer_class = GuideTaskSerializer


class GuideKitViewSet(ModelViewSet):
    """Представление набора задач для гайда."""
    queryset = GuideKit.objects.all()
    serializer_class = GuideKitSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return GuideKitCreateUpdateSerializer
        return  GuideKitSerializer


class GuideStatusViewSet(ModelViewSet):
    """Представление статуса гайда."""
    queryset = GuideStatus.objects.all()
    serializer_class = GuideStatusSerializer


class GuideViewSet(ModelViewSet):
    """Представление гайда."""
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return GuideCreateUpdateSerializer
        return GuideSerializer

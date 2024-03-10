from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.content_serializers import (
    ContentCreateSerializer,
    ContentUpdateSerializer,
    ContentPageSerialzier,
    # ContentPageUpdateSerializer,
    ContentSerializer,
    GuideCreateUpdateSerializer,
    GuideKitCreateUpdateSerializer,
    GuideKitSerializer,
    GuideSerializer,
    GuideTaskSerializer,
    MerchPhotoSerializer,
)
from api.mixins import DestroyWithPayloadMixin
from content.models import Content, Guide, GuideKit, GuideTask, MerchPhoto


class GuideTaskViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление задачи для гайда."""

    queryset = GuideTask.objects.all()
    serializer_class = GuideTaskSerializer


class GuideKitViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление набора задач для гайда."""

    queryset = GuideKit.objects.all()
    serializer_class = GuideKitSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return GuideKitCreateUpdateSerializer
        return GuideKitSerializer


class GuideViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление гайда."""

    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return GuideCreateUpdateSerializer
        return GuideSerializer


class MerchPhotoViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Преставление для сущности Фото в мерче."""

    queryset = MerchPhoto.objects.all()
    serializer_class = MerchPhotoSerializer


class ContentViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление для контента."""

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_queryset(self):
        params = self.request.query_params
        if "ambassador" in params:
            if "is_guide_content" in params:
                return Content.objects.filter(
                    is_guide_content=params["is_guide_content"],
                    ambassador=params["ambassador"],
                )
            return Content.objects.filter(
                    ambassador=params["ambassador"],
                )
        return Content.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ContentCreateSerializer
        if self.action == "partial_update":
            return ContentUpdateSerializer
        return ContentSerializer


class ContentPageViewSet(ModelViewSet):
    """Представление для страницы контент со списком амбассадоров."""

    queryset = Ambassador.objects.all()
    serializer_class = ContentPageSerialzier
    http_method_names = ['get', 'patch']

    # def get_serializer_class(self):
    #     if self.action == 'partial_update':
    #         return ContentPageUpdateSerializer
    #     return ContentPageSerialzier

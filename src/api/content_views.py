from rest_framework.viewsets import ModelViewSet

from api.mixins import DestroyWithPayloadMixin
from api.content_serializers import GuideSerializer, GuideCreateUpdateSerializer, GuideKitSerializer, GuideTaskSerializer, GuideKitCreateUpdateSerializer, MerchPhotoSerializer, ReviewSerializer, ReviewPlatformSerializer
from content.models import Guide, GuideKit, GuideTask, MerchPhoto, Review, ReviewPlatfrom


class GuideTaskViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление задачи для гайда."""
    queryset = GuideTask.objects.all()
    serializer_class = GuideTaskSerializer


class GuideKitViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление набора задач для гайда."""
    queryset = GuideKit.objects.all()
    serializer_class = GuideKitSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return GuideKitCreateUpdateSerializer
        return GuideKitSerializer


class GuideViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление гайда."""
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return GuideCreateUpdateSerializer
        return GuideSerializer


class MerchPhotoViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Преставление для сущности Фото в мерче."""
    queryset = MerchPhoto.objects.all()
    serializer_class = MerchPhotoSerializer


class ReviewPlaformViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление платформы для отзыва."""
    queryset = ReviewPlatfrom.objects.all()
    serializer_class = ReviewPlatformSerializer


class ReviewViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Преставление для отзыва."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

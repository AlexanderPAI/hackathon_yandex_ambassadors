from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.content_serializers import (  # ContentPageUpdateSerializer,
    ContentCreateSerializer,
    ContentPageSerialzier,
    ContentSerializer,
    ContentUpdateSerializer,
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

    def get_queryset(self):
        return GuideKitSerializer.setup_eager_loading(GuideKit.objects.all())


ambassador = openapi.Parameter(
    "ambassador",
    openapi.IN_QUERY,
    description=("ambassador"),
    type=openapi.TYPE_INTEGER,
)


@method_decorator(
    name="list", decorator=swagger_auto_schema(manual_parameters=[ambassador])
)
class GuideViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """Представление гайда."""

    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return GuideCreateUpdateSerializer
        return GuideSerializer

    def get_queryset(self):
        params = self.request.query_params
        all_guides = GuideSerializer.setup_eager_loading(Guide.objects.all())
        if "ambassador" in params:
            return all_guides.filter(
                ambassador=params["ambassador"],
            )
        return all_guides


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
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return ContentPageSerialzier.setup_eager_loading(Ambassador.objects.all())

    # def get_serializer_class(self):
    #     if self.action == 'partial_update':
    #         return ContentPageUpdateSerializer
    #     return ContentPageSerialzier

from rest_framework.viewsets import ModelViewSet

from content.models import GuideTask, GuideKit, GuideTaskGuideKit, GuideStatus, Guide, MerchPhoto, ReviewPlatfrom, Review, ContentPlatform, Content
from api.content_serializers import GuideSerializer, GuideTaskSerializer, GuideKitSerializer, GuideTaskGuideKitSerializer


class GuideTaskViewSet(ModelViewSet):
    queryset = GuideTask.objects.all()
    serializer_class = GuideTaskSerializer


class GuideKitViewSet(ModelViewSet):
    queryset = GuideKit.objects.all()
    serializer_class = GuideKitSerializer


class GuideViewSet(ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

from rest_framework.viewsets import ModelViewSet

from api.content_serializers import (  # GuideTaskGuideKitSerializer,
    GuideKitSerializer,
    GuideSerializer,
    GuideTaskSerializer,
)
from content.models import Guide, GuideKit, GuideTask

# Content,; ContentPlatform,; GuideStatus,; GuideTaskGuideKit,; MerchPhoto,; Review,;
# ReviewPlatfrom,


class GuideTaskViewSet(ModelViewSet):
    queryset = GuideTask.objects.all()
    serializer_class = GuideTaskSerializer


class GuideKitViewSet(ModelViewSet):
    queryset = GuideKit.objects.all()
    serializer_class = GuideKitSerializer


class GuideViewSet(ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

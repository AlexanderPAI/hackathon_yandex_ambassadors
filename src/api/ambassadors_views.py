from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.ambassadors_serializers import (
    AmbassadorCreateSerializer,
    AmbassadorReadSerializer,
)


# TODO: n+1 problen
class AmbassadorViewSet(ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorReadSerializer

    serializer_action_classes = {
        "list": AmbassadorReadSerializer,
        "retrieve": AmbassadorReadSerializer,
        "create": AmbassadorCreateSerializer,
        "update": AmbassadorCreateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super().get_serializer_class()

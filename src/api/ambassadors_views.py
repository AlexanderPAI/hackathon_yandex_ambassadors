from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .mixins import DestroyWithPayloadMixin
from ambassadors.models import Ambassador
from api.ambassadors_serializers import (
    AmbassadorCreateSerializer,
    AmbassadorReadSerializer,
    AmbassadorUpdateSerializer,
)


class AmbassadorViewSet(DestroyWithPayloadMixin, ModelViewSet):
    """ViewSet for Ambassadors
    By default sorted by created date (created field) from new to old.
    Sorting by fields: "created", "email", "phone_number", "telegram_id".
    Searching by field: "name".
    Filtering by fields: "status", "name", "gender", "onboarding_status",
    "program", "country", "city", "activity".
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorReadSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter,)
    filter_fields = ("status", "name", "gender", "onboarding_status", "program",
                     "country", "city", "activity",)
    search_fields = "name"
    ordering_fields = ("created", "email", "phone_number", "telegram_id",)

    serializer_action_classes = {
        "list": AmbassadorReadSerializer,
        "retrieve": AmbassadorReadSerializer,
        "create": AmbassadorCreateSerializer,
        "update": AmbassadorUpdateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super().get_serializer_class()

    def get_queryset(self):
        queryset = AmbassadorReadSerializer.setup_eager_loading(
            Ambassador.objects.all()
        )
        return queryset.order_by("-created")

from django.contrib.admin.models import LogEntry
from rest_framework import viewsets

from .user_actions_serializers import UserActionsSerializer


class UserActionsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user actions."""

    queryset = LogEntry.objects.all()
    serializer_class = UserActionsSerializer

from django.contrib.admin.models import LogEntry
from rest_framework import serializers


class UserActionsSerializer(serializers.ModelSerializer):
    """Serializer for user actions."""

    class Meta:
        model = LogEntry
        fields = "__all__"

from rest_framework import permissions


class IsTutorOrReadOnly(permissions.BasePermission):
    """Allows only the tutor to edit and delete merch applications."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and obj.tutor == request.user
        )

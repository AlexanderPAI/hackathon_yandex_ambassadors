from rest_framework import response, status

from .promo_serializers import DestroyObjectSuccessSerializer

MESSAGE_ON_DELETE = "Строка удалена"


class DestroyWithPayloadMixin(object):
    """Mixin to provide json response after delete requests."""

    def destroy(self, *args, **kwargs):
        super().destroy(*args, **kwargs)
        return response.Response(
            DestroyObjectSuccessSerializer({"message": MESSAGE_ON_DELETE}).data,
            status=status.HTTP_200_OK,
        )

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .promo_views import MerchApplicationViewSet

app_name = "api"

router = DefaultRouter()

router.register("merch_applications", MerchApplicationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

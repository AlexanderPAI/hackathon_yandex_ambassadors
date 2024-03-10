from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .ambassadors_views import AmbassadorViewSet
from .promo_views import (
    MerchApplicationViewSet,
    MerchCategoryViewSet,
    MerchViewSet,
    PromocodeViewSet,
)
from .user_actions_views import UserActionsViewSet
from api.content_views import ContentViewSet, ContentPageViewSet, GuideKitViewSet, GuideTaskViewSet, GuideViewSet, MerchPhotoViewSet

app_name = "api"

router = DefaultRouter()

# Merch
router.register("merch_category", MerchCategoryViewSet)
router.register("merch_price", MerchViewSet)
router.register("send_merch", MerchApplicationViewSet)

# Ambassadors
router.register("ambassadors", AmbassadorViewSet)
router.register("promocodes", PromocodeViewSet)

# History
router.register("edit_history", UserActionsViewSet)

# Guides
router.register("guides", GuideViewSet)
router.register("guide_tasks", GuideTaskViewSet)
router.register("guide_kits", GuideKitViewSet)
router.register("merch_photo", MerchPhotoViewSet)

# Content
router.register("merch_photo", MerchPhotoViewSet)
router.register("content", ContentViewSet)
router.register("content_page", ContentPageViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Hackathon Yandex Ambassadors Team 04 API",
        default_version="v1",
        description="API documentation for the Hackathon Yandex Ambassadors project",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="hackathonyacrm@yandex.kz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

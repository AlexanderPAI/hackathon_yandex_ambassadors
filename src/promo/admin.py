from django.contrib import admin
from django.db.models import F, Prefetch, Sum

from .models import (
    Merch,
    MerchApplication,
    MerchCategory,
    MerchInApplication,
    Promocode,
)


class MerchInApplicationInline(admin.TabularInline):
    """Displays merch items in a particular merch application."""

    model = MerchInApplication
    extra = 0


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    """Displays merch species in admin panel."""

    list_display = ["pk", "name", "category", "slug", "size", "cost"]
    list_display_links = ["name"]
    search_fields = ["name", "slug"]
    list_filter = ["category", "size", "cost"]
    ordering = ["pk"]


@admin.register(MerchCategory)
class MerchCategoryAdmin(admin.ModelAdmin):
    """Displays merch categories in admin panel."""

    list_display = ["pk", "name", "slug"]
    list_display_links = ["name"]
    search_fields = ["name", "slug"]
    ordering = ["pk"]


@admin.register(MerchApplication)
class MerchApplicationAdmin(admin.ModelAdmin):
    """Displays applications for sending merch to ambassadors in admin panel."""

    list_display = [
        "pk",
        "application_number",
        "ambassador",
        "tutor",
        "created",
        "merch_cost",
    ]
    list_display_links = ["application_number"]
    list_filter = ["tutor", "created"]
    search_fields = ["application_number", "ambassador"]
    inlines = [MerchInApplicationInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related(
            Prefetch(
                "merch_in_applications",
                queryset=MerchInApplication.objects.select_related("merch"),
            )
        ).annotate(
            merch_cost=Sum(
                F("merch_in_applications__quantity")
                * F("merch_in_applications__merch__cost"),
                default=0,
            ),
        )

    @admin.display(description="Merch cost", ordering="merch_cost")
    def merch_cost(self, obj):
        return obj.merch_cost


@admin.register(MerchInApplication)
class MerchInApplicationAdmin(admin.ModelAdmin):
    """Displays m2m connections between the merch applications and merch species."""

    list_display = ["pk", "application", "merch", "quantity"]
    list_display_links = ["application"]
    list_filter = ["quantity", "merch"]


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    """Displays promocodes in admin panel."""

    list_display = ["pk", "code", "ambassador", "created", "is_active"]
    list_display_links = ["code"]
    search_fields = ["code", "ambassador"]  # TODO: change to "ambassador__name"
    list_filter = ["is_active", "created"]
    ordering = ["pk"]

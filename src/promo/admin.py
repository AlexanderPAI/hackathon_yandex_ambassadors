from django.contrib import admin

from .models import Merch, MerchCategory, Promocode


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    """Class to display merch species in admin panel."""

    list_display = ["pk", "name", "category", "slug", "size", "cost"]
    list_display_links = ["name"]
    search_fields = ["name", "slug"]
    list_filter = ["category", "size", "cost"]
    ordering = ["pk"]


@admin.register(MerchCategory)
class MerchCategoryAdmin(admin.ModelAdmin):
    """Class to display merch categories in admin panel."""

    list_display = ["pk", "name", "slug"]
    list_display_links = ["name"]
    search_fields = ["name", "slug"]
    ordering = ["pk"]


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    """Class to display promocodes in admin panel."""

    list_display = ["pk", "code", "ambassador", "created", "is_active"]
    list_display_links = ["code"]
    search_fields = ["code", "ambassador"]  # TODO: change to "ambassador__username"
    list_filter = ["is_active", "created"]
    ordering = ["pk"]

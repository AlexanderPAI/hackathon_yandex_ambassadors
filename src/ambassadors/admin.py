from django.contrib import admin

from .models import Activity, Address, Ambassador, AmbassadorPurpose, Program, Purpose, \
    Status


@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    """Add Ambassador to admin panel"""

    list_display = (
        "pk",
        "name",
        "status",
        "tutor",
    )
    list_display_links = ("name",)
    list_filter = ("program", "status")
    ordering = ("-created",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("status", "program")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("pk", "postal_code", "country", "city", "street")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Add Program to admin panel"""

    list_display = ("pk", "name", "slug")
    list_display_links = ("name",)


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    """Add Purpose to admin panel"""

    list_display = ("pk", "name", "slug")
    list_display_links = ("name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Add Status to admin panel"""

    list_display = ("pk", "name", "slug")
    list_display_links = ("name",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Add Activity to admin panel"""

    list_display = ("pk", "name", "slug")
    list_display_links = ("name",)


@admin.register(AmbassadorPurpose)
class AmbassadorPurposeAdmin(admin.ModelAdmin):
    """Add AmbassadorPurpose to admin panel"""

    list_display = ("ambassador", "purpose", "personal_purpose")
    list_display_links = ("ambassador", "purpose",)

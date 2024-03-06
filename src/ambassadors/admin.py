from django.contrib import admin

from .models import Activity, Address, Ambassador, Group, Program, Purpose, Status


@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    """Add Ambassador to admin panel"""

    list_display = (
        "pk",
        "name",
        "status",
        "tutor",
    )
    # exclude = ("address",)
    list_display_links = ("name",)
    list_filter = ("program", "status")
    ordering = ("-created",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("pk", "postal_code", "country", "city", "street")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Add Group to admin panel"""

    list_display = ("name",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Add Program to admin panel"""

    list_display = ("name",)


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    """Add Purpose to admin panel"""

    list_display = ("name", "description")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Add Status to admin panel"""

    list_display = ("name",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Add Activity to admin panel"""

    list_display = ("name",)

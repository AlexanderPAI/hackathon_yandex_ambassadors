from django.contrib import admin

from content.models import (
    Content,
    Guide,
    GuideKit,
    GuideTask,
    GuideTaskGuideKit,
    MerchPhoto,
)


class GuideTasksInGuideKitsInLine(admin.TabularInline):
    model = GuideTaskGuideKit
    extra = 1


@admin.register(GuideTask)
class GuideTaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "type",
    ]


@admin.register(GuideKit)
class GuideKitAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    inlines = [GuideTasksInGuideKitsInLine]


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "ambassador",
        "guide_kit",
        "status",
    ]
    search_fields = ["ambassador", "guide_kit"]


@admin.register(MerchPhoto)
class MerchPhotoAdmin(admin.ModelAdmin):
    list_display = ["id", "ambassador"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ambassador",
        "created",
        "platform",
        "type",
        "link",
        "is_guide_content",
    ]

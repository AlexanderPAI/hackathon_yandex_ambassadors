from django.contrib import admin

from content.models import (
    Content,
    ContentPlatform,
    Guide,
    GuideKit,
    GuideStatus,
    GuideTask,
    GuideTaskGuideKit,
    MerchPhoto,
    Review,
    ReviewPlatfrom,
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


@admin.register(GuideStatus)
class GuideStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    search_fields = ["name"]


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


@admin.register(ReviewPlatfrom)
class ReviewPlatformAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ambassador",
        "platform",
        "link",
    ]
    search_fields = ["ambassador"]
    list_filter = ["platform"]


@admin.register(ContentPlatform)
class ContentPlatform(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ambassador",
        "created",
        "platform",
        "link",
        "is_guide_content",
    ]

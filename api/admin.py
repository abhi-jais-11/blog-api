from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "created_at", "image_preview")
    list_filter = ("category", "tags", "created_at", "author")
    search_fields = ("title", "body", "author__username", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)           # faster lookup for large user tables
    filter_horizontal = ("tags",)         # nice UI for many-to-many
    readonly_fields = ("image_preview",)  # preview only

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "author", "category", "tags", "body")
        }),
        ("Media", {
            "fields": ("image", "image_preview"),
        }),
        ("Dates", {
            "fields": ("created_at",),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height:200px; object-fit: contain;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Preview"

from django.contrib import admin
from .models import Paragraph, Performance


@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ("text_preview", "difficulty", "duration", "created_at")
    list_filter = ("difficulty", "duration", "created_at")
    search_fields = ("text",)
    ordering = ("-created_at",)  # newest first

    def text_preview(self, obj):
        """Short preview of paragraph text"""
        return (obj.text[:50] + "...") if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Paragraph"


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "wpm",
        "accuracy",
        "errors",
        "difficulty",
        "duration",
        "date",
    )
    list_filter = ("difficulty", "duration", "date", "user")
    search_fields = ("user__username",)
    ordering = ("-date",)  # newest performance first
    readonly_fields = ("date",)  # prevent editing performance date manually

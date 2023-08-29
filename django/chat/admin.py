from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django_admin_inline_paginator.admin import TabularInlinePaginated

from .models import Message, Room


class MessageInline(TabularInlinePaginated):
    model = Message
    extra = 0
    per_page = 10
    ordering = ["created_at"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    filter_horizontal = ["member_set"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["author", "truncated_text"]
    list_display_links = ["truncated_text"]
    list_filter = ["author", "room"]

    @admin.display
    def truncated_text(self, obj: Message):
        return truncatechars(obj.text, 15)

from django.contrib import admin
from .models import Replies


@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'updated', 'active']
    list_filter = ['created', 'updated']

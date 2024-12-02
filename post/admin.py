from django.contrib import admin
from .models import Post



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'active', 'polarity', 'created', 'updated', 'edited']
    list_filter = ['id', 'author', 'active', 'polarity']
    list_per_page = 10
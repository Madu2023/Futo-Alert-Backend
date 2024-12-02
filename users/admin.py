from django.contrib import admin
from .models import User




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''Admin View for ModelName'''

    list_display = ('username', 'first_name', 'last_name', 'email', 'post_polarity', 'comment_polarity', 'reply_polarity', 'phone_number', 'is_superuser', 'is_active', 'created', 'updated')
    list_filter = ('username', 'email', 'phone_number', 'created', 'updated')
    search_fields = ('username',)
    
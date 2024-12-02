from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ValidationError


class UserPostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        
        return obj.author == request.user
    
    def has_permission(self, request, view):
        if request.user.is_active == False:
            return False
        elif request.user.is_anonymous:
            return request.method in SAFE_METHODS
        elif request.user and request.user.is_authenticated:
            return True
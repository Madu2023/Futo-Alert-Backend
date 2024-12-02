from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
    def get_object(self):
        obj = User.objects.get_user_by_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj



from auths.viewsets.login import LoginViewSet
from auths.viewsets.refresh import RefreshViewSet
from auths.viewsets.viewsets import UserRegisterViewSet
from comments.viewsets import CommentViewSet
from post.viewsets import PostViewSet
from replies.viewsets import ReplyViewSet
from rest_framework import routers
from django.urls import path, include

from users.viewsets import UserViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='users'),
router.register(r'auth/register', UserRegisterViewSet, basename='auth-register'),
router.register(r'auth/login', LoginViewSet, basename='auth-login'),
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh'),
router.register(r'post',  PostViewSet, basename='post'),
router.register(r'comment', CommentViewSet, basename='comment'),
router.register(r'reply', ReplyViewSet, basename='replies')
                





urlpatterns = [
    *router.urls
    
]
from .models import Post
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from textblob import TextBlob
from .permissions import UserPostPermission
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [UserPostPermission,]
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    
    
    def get_queryset(self):
        return Post.objects.filter(active=True).order_by('-created')
    
    
    def get_object(self):
        obj = Post.objects.get_object_by_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
        
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.post_polarity > 10:
            return Response({
                "error": "Account Was Banned By you going Against Our Community Standard"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = request.data["text"]
        print("This is the text body", text)
        print("This is the data", request.data)
        sentiment_analysis = TextBlob(text)
        if sentiment_analysis.sentiment.polarity > 0:
            print("This is the polarity", sentiment_analysis.sentiment.polarity)
            request.data["polarity"] = True
            serializer.save(polarity=True)
        elif sentiment_analysis.sentiment.polarity < 0:
            print("This is the polarity", sentiment_analysis.sentiment.polarity)
            user.post_polarity += 1
            print("This is the users polarity", user.post_polarity)
            user.save()
            serializer.save(polarity=False) 

            
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def post_like(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        post_like = user.like_post(post)
        post_serializer = self.serializer_class(post_like)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def post_unlike(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        post_like = user.unlike_post(post)
        post_serializer = self.serializer_class(post_like)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def post_love(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        post_like = user.love_post(post)
        post_serializer = self.serializer_class(post_like)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def post_unlove(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        post_like = user.unlove_post(post)
        post_serializer = self.serializer_class(post_like)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    
    
           
    
    
    
    

    



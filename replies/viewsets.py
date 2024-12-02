from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import ReplySerializer
from rest_framework.permissions import IsAuthenticated
from .models import Replies
from textblob import TextBlob
from .permissions import UserReplyPermission


class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    http_method_names = ['get', 'put', 'post', 'patch', 'delete']
    permission_classes = [UserReplyPermission, IsAuthenticated, ]
    
    
    def get_queryset(self):
        return Replies.objects.filter(active=True)
    
    def get_object(self):
        obj = Replies.objects.get_object_by_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.reply_polarity > 10:
            user.is_active = False
            user.save()
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

            
        return Response(serializer.data, status=status.HTTP_201_CREATED)



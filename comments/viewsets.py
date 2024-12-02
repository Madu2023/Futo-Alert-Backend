from rest_framework import viewsets
from .serializers import CommentSerializer
from .models import Comment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from textblob import TextBlob
from rest_framework.response import Response
from rest_framework import status
from .permissions import UserCommentPermission


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [UserCommentPermission, IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(active=True).order_by('-created')
    
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.comment_polarity > 10:
            user.is_active = False
            user.save()
            return Response({
                "error": "Account Was Banned By you going Against Our Community Standard"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = request.data["comment"]
        print("This is the text body", comment)
        print("This is the data", request.data)
        sentiment_analysis = TextBlob(comment)
        if sentiment_analysis.sentiment.polarity > 0:
            request.data["polarity"] = True
            serializer.save(author=user, polarity=True)
        elif sentiment_analysis.sentiment.polarity < 0:
            request.data["polarity"] = False
            user.comment_polarity += 1
            print("This is the users polarity", user.comment_polarity)
            user.save()
            serializer.save(author=user, polarity=False) 

            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



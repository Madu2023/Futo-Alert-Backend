from rest_framework import serializers
from .models import Replies
from comments.models import Comment
from users.models import User
from replies.models import Replies
from users.serializers import UserSerializer
from comments.serializers import CommentSerializer
from django.core.exceptions import ValidationError



class ReplySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    comment = serializers.SlugRelatedField(queryset=Comment.objects.all(), slug_field='id')
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    
    
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You Can Not Reply For Another User")
        return value
    
    
    def update(self, instance, validated_data):
        if instance.edited == False:
            validated_data["edited"] = True
        
        instance = super().update(instance, validated_data)
        return instance    
            
    
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_user_by_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        comment = Comment.objects.get_comment_object_by_id(rep["comment"])
        rep["comment"] = CommentSerializer(comment).data
        return rep
    
    class Meta:
        model = Replies
        fields = ["id", "comment", "author", "created", "updated", 'text', "edited", "polarity", "active"]
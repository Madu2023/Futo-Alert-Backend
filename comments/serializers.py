from rest_framework import serializers
from .models import Comment
from post.models import Post
from users.models import User
from post.serializers import PostSerializer
from users.serializers import UserSerializer
from users.models import User
from django.core.exceptions import ValidationError

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='id')
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    
    def get_replies_count(self, instance):
        return instance.replies.count()
    
    
    
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You Cannot Create A Comment For Another User")
        
    def update(self, instance, validated_data):
        if instance.edited == False:
            validated_data["edited"] = True
        instance = super().update(instance, validated_data)
        return instance    
                
        
        
    
    
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        post = Post.objects.get_object_by_id(rep["post"])
        rep["post"] = PostSerializer(post).data
        author = User.objects.get_user_by_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep
    
   
    
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'comment', 'author', 'replies_count', 'created', 'updated', 'edited', 'polarity']
        
        
        
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer
from .models import Post
from django.core.exceptions import ValidationError




class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    post_likes = serializers.SerializerMethodField()
    post_loves = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    def get_post_likes(self, instance):
        """
        A Method to get the number of likes a post have
        """
        return instance.liked_by.count()
    
    
    def get_post_loves(self, instance):
        """
        A method to count how many post that have been loved by a user
        """
        return instance.loved_by.count()
    
    
    def get_comment_count(self, instance):
        """
        A Method to return number of comments in a post
        """
        return instance.comments.count()
    
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You Cannot Create A Post For Another User")
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_user_by_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep
    
    def update(self, instance, validated_data):
        if instance.edited == False:
            validated_data["edited"] = True
        update = super().update(instance, validated_data)
        return update    
    
            
    
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created', 'post_likes', 'post_loves', 'comment_count', 'updated', 'edited', 'polarity']
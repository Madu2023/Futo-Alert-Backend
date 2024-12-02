from rest_framework import serializers
from .models import User




class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    followers = serializers.SerializerMethodField()
    
    def get_followers(self, instance):
        return instance.user_followers_count()
    
        
        
    
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'followers',  'email', 'phone_number', 'image', 'created', 'updated']
    
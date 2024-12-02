from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    id  = serializers.UUIDField(format='hex', read_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'image', 'password', 'created', 'updated']
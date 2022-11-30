from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class postSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True) 
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'created_at']





from rest_framework import serializers
from .models import Post, Category
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class postSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'category', 'created_at']





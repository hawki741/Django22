from rest_framework import serializers
from .models import Post

class postSerializer(serializers.ModelSerializer):
    # company = serializers.ReadOnlyField(source="author.username")
    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at']

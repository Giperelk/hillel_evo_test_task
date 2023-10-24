from rest_framework import serializers
from socnet.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'likes_count']

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostDetailSerializer(ModelSerializer):
    """
    Post의 CRUD를 위한 data를 들고온다.
    title, content, profile
    """

    class Meta:
        model = Post
        fields = ('title', 'content', 'profile')


class PostListSerializer(ModelSerializer):
    """
    Post list를 불러오기 위한
    title, summary, profile등을 불러온다
    """
    summary = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('title', 'summary', 'profile')
from rest_framework import serializers
from posts.models import Post, Comment
from users.models import CustomUser
from rest_framework.fields import CurrentUserDefault, ReadOnlyField
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username"]


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "created_date"]


class CommentSerializer(serializers.ModelSerializer):

    post = serializers.StringRelatedField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "description", "published", "create_date"]
        read_only_fields = ["id", "author", "create_date"]


class PostListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer(read_only=True)
    formatted_date = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_formatted_date(self, obj):
        return obj.create_date.strftime("%d-%m-%Y %H:%M")

    class Meta:
        model = Post
        fields = "__all__"

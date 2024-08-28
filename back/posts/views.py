from datetime import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from posts.models import Post, Comment
from rest_framework import generics
from posts.serializers import (
    PostListSerializer,
    PostCreateSerializer,
    CommentCreateSerializer,
    CommentSerializer,
)
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from .permissions import IsAdminOrOwner


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all().order_by("-create_date")

    def get_permissions(self):
        # Определяем разрешения для разных HTTP методов
        if self.request.method == "GET":
            # Для GET запросов разрешаем всем
            permission_classes = [AllowAny]
        elif self.request.method == "POST":
            # Для POST запросов разрешаем только аутентифицированным
            permission_classes = [IsAuthenticated]
        else:
            # Для других методов можно указать аналогичное разрешение
            permission_classes = [IsAdminOrOwner]  # Можно настроить по необходимости

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostListSerializer
        return PostCreateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = request.user
        id = Post.objects.count() + 1
        self.perform_create(serializer, author, id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, author, id):
        print(f"Creating post with data: {serializer.validated_data}")
        serializer.save(author=author, id=id)


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all().order_by("-created_date")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentSerializer
        return CommentCreateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = request.user
        created_date = datetime.now()
        self.perform_create(serializer, author, created_date)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer, author, created_date):
        print(f"Creating post with data: {serializer.validated_data}")
        serializer.save(author=author, created_date=created_date)

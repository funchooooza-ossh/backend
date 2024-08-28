from django.contrib import admin
from django.urls import path, include
from posts.views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from main.views import PostListView, PostCreateView


api_router = DefaultRouter()
api_router.register("apiv1post", PostViewSet, basename="apiv1post")
api_router.register("apiv1comment", CommentViewSet, basename="apiv1comment")


urlpatterns = [
    path("post/", PostListView.post_list, name="postlist"),
    path("post/create/", PostCreateView.create_post, name="postcreate"),
    path("post/<int:pk>/", PostListView.post_detail, name="detail"),
    path("post/edit/<int:pk>/", PostCreateView.edit_post, name="edit"),
    path("post/delete/<int:pk>/", PostCreateView.delete_post, name="delete"),
    path("", include("users.urls")),
]

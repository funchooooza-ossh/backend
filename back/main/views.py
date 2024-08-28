import time
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from posts.models import Post, Comment
import requests
from rest_framework.response import Response
from datetime import datetime
from .forms import PostCreateForm, CommentCreateForm
from rest_framework.authtoken.models import Token


class PostListView:
    def post_list(request):
        api_url = request.build_absolute_uri("/api/post/")
        response = requests.get(api_url)
        posts = response.json()
        return render(request, "main/list.html", {"posts": posts})

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=pk)
        if request.user.is_authenticated:
            if request.method == "POST":
                form = CommentCreateForm(request.POST)
                if form.is_valid():
                    description = form.cleaned_data["description"]
                    author = request.user.id
                    token, created = Token.objects.get_or_create(user=author)
                    url = request.build_absolute_uri(f"/api/comment/")

                    headers = {"Authorization": "Token " + token.key}

                    data = {"author": author, "post": pk, "description": description}
                    response = requests.post(url, headers=headers, json=data)
                    if response.status_code == 201:
                        return redirect("detail", pk)
                    else:
                        return render(
                            request,
                            "main/detail.html",
                            {"form": form, "error": response.text},
                        )
            else:
                post = get_object_or_404(Post, pk=pk)
                form = CommentCreateForm()
                comments = Comment.objects.filter(post_id=pk)
                return render(
                    request,
                    "main/detail.html",
                    {"post": post, "form": form, "comments": comments},
                )
        else:
            return HttpResponse("Please login to see post details")


class PostCreateView:
    def create_post(request):
        if request.user.is_authenticated:
            if request.method == "POST":
                form = PostCreateForm(request.POST)
                if form.is_valid():

                    author = request.user.id
                    title = form.cleaned_data["title"]
                    description = form.cleaned_data["description"]
                    published = form.cleaned_data["published"]

                    api_url = request.build_absolute_uri("/api/post/")
                    token, created = Token.objects.get_or_create(user=author)
                    headers = {"Authorization": "Token " + token.key}
                    data = {
                        "author": author,
                        "title": title,
                        "description": description,
                        "published": published,
                    }
                    response = requests.post(api_url, headers=headers, json=data)
                    if response.status_code == 201:
                        return redirect("postlist")
                    else:
                        return render(
                            request,
                            "main/create.html",
                            {"form": form, "errors": response.text},
                  
                        )
            else:
                form = PostCreateForm()
                return render(request, "main/create.html", {"form":form})
        else:
            return HttpResponse("You are not logged in")

    def edit_post(request, pk):
        if request.user.is_authenticated:
            if request.method == "POST":
                post = get_object_or_404(Post, pk=pk)
                if request.user == post.author or request.user.is_staff:
                    form = PostCreateForm(request.POST)
                    if form.is_valid():
                        author = request.user.id
                        title = form.cleaned_data["title"]
                        description = form.cleaned_data["description"]
                        published = form.cleaned_data["published"]

                        api_url = request.build_absolute_uri(f"/api/post/{pk}/")
                        token, created = Token.objects.get_or_create(user=author)
                        headers = {"Authorization": "Token " + token.key}
                        data = {
                            "id": pk,
                            "author": author,
                            "title": title,
                            "description": description,
                            "published": published,
                        }
                        response = requests.patch(api_url, headers=headers, json=data)
                        if response.status_code == 200:
                            return redirect("detail", pk)
                        else:
                            return render(
                                request,
                                "main/create.html",
                                {"form": form, "error": response.text},
                            )
                else:
                    return HttpResponse("You are now allowed")

            else:
                post = get_object_or_404(Post, pk=pk)
                if request.user == post.author or request.user.is_staff:
                    form = PostCreateForm(instance=post)
                    return render(request, "main/create.html", {"form": form})

    def delete_post(request, pk):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=pk)
            if request.user == post.author or request.user.is_staff:
                author = request.user.id
                token, created = Token.objects.get_or_create(user=author)
                url = request.build_absolute_uri(f"/api/post/{pk}/")
                headers = {"Authorization": "Token " + token.key}
                response = requests.delete(url, headers=headers)
                if (
                    response.status_code == 200
                    or response.status_code == 202
                    or response.status_code == 204
                ):
                    return redirect("postlist")
                else:
                    return redirect("detail", pk)
            else:
                return HttpResponse("You are now allowed")
        return HttpResponse("You are not logged in")

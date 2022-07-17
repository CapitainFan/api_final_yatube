from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from posts.models import Group, Post
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          FollowSerializer)
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .mypaginations import MyLimitOffsetPagination


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MyLimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    pagination_class = MyLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = MyLimitOffsetPagination

from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from posts.models import Group, Post, User
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          FollowSerializer)
from .permissions import IsOwnerOrReadOnly, ReadOnly
from rest_framework.permissions import IsAuthenticated
from .mypaginations import MyLimitOffsetPagination


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = (IsOwnerOrReadOnly, )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    pagination_class = MyLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    permission_classes = (IsAuthenticated, )
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import viewsets, filters, serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow, User
from .serializers import (
    PostSerializer, CommentSerializer,
    GroupSerializer, FollowSerializer, UserSerializer
)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Для автоматического формирования поля 'author' при создании поста"""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('title',)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment"""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def get_queryset(self):
        """Получаем комментарии только к посту с post_id из запроса"""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """
        Для автоматического формирования поля 'author'
        при создании комментария
        """
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Group"""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAuthenticated,)
    search_fields = ('user__username', 'following__username',)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """Формирует данные о подписках пользователя"""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Задает значение поля user"""
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

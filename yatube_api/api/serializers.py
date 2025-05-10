from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post"""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('pub_date', )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('created', )


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group"""

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow"""
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
        read_only_fields = ('user',)

    def create(self, validated_data):
        """
        В методе создается запись в базу данных на основе получаемого
        при POST-запросе значения поля 'following'
        """
        username = validated_data['following']
        following = get_object_or_404(User, username=username)
        return Follow.objects.create(
            user=self.context['request'].user,
            following=following
        )

    def validate_following(self, value):
        """
        В методе проверяется и сключается возможность подписаться
        на самого себя или на другого пользователя повторно
        """
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        elif Follow.objects.filter(user=user, following=value).exists():
            raise serializers.ValidationError(
                f'Вы уже подписаны на {value}!'
        )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        model = User
        fields = ('id', 'username')

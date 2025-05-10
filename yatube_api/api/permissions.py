from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает только авторам изменять или удалять объекты
    """

    def has_object_permission(self, request, view, obj):
        """
        Безопасные методы из SAFE_METHODS разрешены для всех пользователей,
        остальные методы - только для авторов
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

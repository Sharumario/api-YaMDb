from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin'
                or request.user.is_superuser
                or request.user.is_staff)


class OwnerOrReadOnly(BasePermission):
    """Пермишен, который разрешает всем просматривать материалы,
    но редактировать только автору.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

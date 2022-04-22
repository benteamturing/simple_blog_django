from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

ADMIN_ROLE = '10'


class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # admin
            if admin_user_perm(request):
                return True
            # object owner
            if object_owner_perm(request, obj):
                return True
            if user_object_perm(request, obj):
                return True

        return False


class IsOwnerOrReadOnly(IsOwnerOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        super().has_object_permission(request, view, obj)


def admin_user_perm(request):
    return request.user.role == ADMIN_ROLE


def object_owner_perm(request, obj):
    if hasattr(obj, 'profile'):
        return obj.profile.user == request.user.id
    return False


def user_object_perm(request, obj):
    if obj.__class__ == get_user_model():
        return obj.id == request.user.id
    return False

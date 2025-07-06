from rest_framework.permissions import BasePermission

from .choices import UserRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.ADMIN


class IsDeliveryMan(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == UserRole.DELIVERY_MAN
        )


class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == UserRole.REGULAR_USER
        )


class IsRegularUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.REGULAR_USER,
            UserRole.ADMIN,
        ]

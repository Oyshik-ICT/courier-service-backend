import logging

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser
from .permissions import IsAdmin
from .serializers import CustomAdminUserSerializer, CustomUserSerializer

logger = logging.getLogger(__name__)


class UserViewset(viewsets.ModelViewSet):
    """Handles operations for regular users and delivery men."""

    queryset = CustomUser.objects.filter(role__in=["REGULAR_USER", "DELIVERY_MAN"])
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_queryset(self):
        try:
            user = self.request.user
            qs = super().get_queryset()
            if not user.is_staff:
                qs = qs.filter(email=user.email)

            return qs
        except Exception:
            logger.exception("Error in UserViewset.get_queryset")
            return CustomUser.objects.none()


class AdminUserViewset(viewsets.ModelViewSet):
    """Handles operations for admin users only."""

    queryset = CustomUser.objects.filter(role="ADMIN")
    serializer_class = CustomAdminUserSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        try:
            obj = super().get_object()

            if (
                self.action in ["update", "partial_update", "destroy"]
                and obj != self.request.user
            ):
                raise PermissionDenied("You can only modify your own profile.")
            return obj
        except Exception:
            logger.exception("Error in AdminUserViewset.get_object")
            raise

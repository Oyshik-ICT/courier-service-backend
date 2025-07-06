from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import UserViewset, AdminUserViewset


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

router = DefaultRouter()
router.register("users", UserViewset, basename="users")
router.register("admin-users", AdminUserViewset, basename="adminusers")

urlpatterns += router.urls
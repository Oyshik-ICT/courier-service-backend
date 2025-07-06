from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import OrderViewset, DeliveryManOrderAPIView


router = DefaultRouter()
router.register("orders-detail", OrderViewset, basename="orders-detail")

urlpatterns = [
    path('delivery/', DeliveryManOrderAPIView.as_view(), name='delivery-orders'),
    path('delivery/<uuid:order_id>/', DeliveryManOrderAPIView.as_view(), name='delivery-order-update'),
]

urlpatterns += router.urls
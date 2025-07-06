from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeliveryManOrderAPIView, OrderViewset

router = DefaultRouter()
router.register("orders-detail", OrderViewset, basename="orders-detail")

urlpatterns = [
    path("delivery/", DeliveryManOrderAPIView.as_view(), name="delivery-orders"),
    path(
        "delivery/<uuid:order_id>/",
        DeliveryManOrderAPIView.as_view(),
        name="delivery-order-update",
    ),
]

urlpatterns += router.urls

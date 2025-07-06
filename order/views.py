import logging

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsDeliveryMan, IsRegularUserOrAdmin

from .models import Order
from .serializers import DeliveryManOrderSerializer, OrderSerializer

logger = logging.getLogger(__name__)


class OrderViewset(viewsets.ModelViewSet):
    """Handles order creation and retrieval for regular users and admins."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsRegularUserOrAdmin]

    def get_queryset(self):
        try:
            user = self.request.user
            qs = super().get_queryset()
            if not user.is_staff:
                qs = qs.filter(sender=user)

            return qs
        except Exception:
            logger.exception("Error in OrderViewset.get_queryset")
            return Order.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save(sender=self.request.user)
        except Exception:
            logger.exception("Error in OrderViewset.perform_create")


class DeliveryManOrderAPIView(APIView):
    """Handles delivery man-specific order listing and status updates."""

    permission_classes = [IsDeliveryMan]

    def get(self, request):
        try:
            orders = Order.objects.filter(delivery_man=request.user)
            serializer = DeliveryManOrderSerializer(orders, many=True)

            return Response(serializer.data)
        except Exception:
            logger.exception("Error in DeliveryManOrderAPIView.get")
            return Response(
                {"detail": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, delivery_man=request.user)
        except Order.DoesNotExist:
            return Response(
                {"details": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            logger.exception("Unexpected error fetching order in patch")
            return Response(
                {"detail": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            serializer = DeliveryManOrderSerializer(
                order, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("Error updating order in DeliveryManOrderAPIView.patch")
            return Response(
                {"detail": "Failed to update order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

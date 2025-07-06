from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer, DeliveryManOrderSerializer
from accounts.permissions import IsRegularUserOrAdmin, IsDeliveryMan
from rest_framework.response import Response
from rest_framework import status

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsRegularUserOrAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_staff:
            qs = qs.filter(sender=user)

        return qs
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class DeliveryManOrderAPIView(APIView):
    permission_classes = [IsDeliveryMan]

    def get(self, request):
        orders = Order.objects.filter(delivery_man=request.user)
        serializer = DeliveryManOrderSerializer(orders, many=True)

        return Response(serializer.data)
    
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, delivery_man=request.user)
        except Order.DoesNotExist:
            return Response(
                {"details": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DeliveryManOrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


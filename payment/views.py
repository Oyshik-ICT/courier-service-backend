from django.conf import settings
import stripe
from rest_framework.views import APIView
from order.models import Order
from rest_framework.response import Response
from rest_framework import status
from order.choices import PaymentStatusChoice, StatusChoice
from django.shortcuts import get_object_or_404
from accounts.permissions import IsRegularUser

class CreateStripeCheckoutSession(APIView):
    permission_classes = [IsRegularUser]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, sender=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if order.payment_status in [PaymentStatusChoice.PAID, PaymentStatusChoice.PAYMENT_PENDING]:
            return Response({"details": f"Payment status is {order.payment_status}"}, status=status.HTTP_400_BAD_REQUEST)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"Delivery for {order.receiver_name}",
                    },
                    'unit_amount': order.price * 100,  # Stripe expects cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'http://localhost:8000/api/v1/payment/payment-success/?order_id={order.order_id}',
            cancel_url=f'http://localhost:8000/api/v1/payment/payment-cancel/?order_id={order.order_id}',
        )

        
        order.payment_id = session.id
        order.payment_status = PaymentStatusChoice.PAYMENT_PENDING
        order.save(update_fields=["payment_id", "payment_status"])

        return Response({'checkout_url': session.url})
    
class PaymentSuccessView(APIView):
    def get(self, request):
        order_id = request.GET.get("order_id")
        order = get_object_or_404(Order, order_id=order_id)
        order.payment_status = PaymentStatusChoice.PAID
        order.status = StatusChoice.CONFIRMED
        order.save(update_fields=["payment_status", "status"])
        return Response({"details": "Payment successful"}, status=status.HTTP_200_OK)

class PaymentCancelView(APIView):
    def get(self, request):
        order_id = request.GET.get("order_id")
        order = get_object_or_404(Order, order_id=order_id)
        order.payment_status = PaymentStatusChoice.UNPAID
        order.status = StatusChoice.PENDING
        order.payment_id = None
        order.save(update_fields=["payment_status", "status", "payment_id"])
        return Response({"details": "Payment was cancelled"}, status=status.HTTP_200_OK)

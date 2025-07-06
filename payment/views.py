import logging

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from accounts.permissions import IsRegularUser
from order.choices import PaymentStatusChoice, StatusChoice
from order.models import Order

logger = logging.getLogger(__name__)


class CreateStripeCheckoutSession(APIView):
    """Creates a Stripe Checkout session for a user's order."""

    permission_classes = [IsRegularUser]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id, sender=request.user)
        except Order.DoesNotExist:
            logger.warning(
                f"Order not found for user {request.user} with ID {order_id}"
            )
            return Response(
                {"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            logger.exception(
                "Unexpected error fetching order in CreateStripeCheckoutSession"
            )
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if order.payment_status in [
            PaymentStatusChoice.PAID,
            PaymentStatusChoice.PAYMENT_PENDING,
        ]:
            return Response(
                {"details": f"Payment status is {order.payment_status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            base_url = settings.BASE_URL

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Delivery for {order.receiver_name}",
                            },
                            "unit_amount": order.price * 100,  # Stripe expects cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"{base_url}/api/v1/payment/payment-success/?order_id={order.order_id}",
                cancel_url=f"{base_url}/api/v1/payment/payment-cancel/?order_id={order.order_id}",
            )

            order.payment_id = session.id
            order.payment_status = PaymentStatusChoice.PAYMENT_PENDING
            order.save(update_fields=["payment_id", "payment_status"])

            return Response({"checkout_url": session.url})
        except Exception:
            logger.exception("Error creating Stripe checkout session")
            return Response(
                {"detail": "Failed to create checkout session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentSuccessView(APIView):
    """Handles post-payment success updates."""

    def get(self, request):
        try:
            order_id = request.GET.get("order_id")
            order = get_object_or_404(Order, order_id=order_id)
            order.payment_status = PaymentStatusChoice.PAID
            order.status = StatusChoice.CONFIRMED
            order.save(update_fields=["payment_status", "status"])
            return Response(
                {"details": "Payment successful"}, status=status.HTTP_200_OK
            )
        except Exception:
            logger.exception("Error handling payment success")
            return Response(
                {"detail": "Failed to update payment success"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentCancelView(APIView):
    """Handles payment cancellation updates."""

    def get(self, request):
        try:
            order_id = request.GET.get("order_id")
            order = get_object_or_404(Order, order_id=order_id)
            order.payment_status = PaymentStatusChoice.UNPAID
            order.status = StatusChoice.PENDING
            order.payment_id = None
            order.save(update_fields=["payment_status", "status", "payment_id"])
            return Response(
                {"details": "Payment was cancelled"}, status=status.HTTP_200_OK
            )
        except Exception:
            logger.exception("Error handling payment cancellation")
            return Response(
                {"detail": "Failed to update payment cancellation"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

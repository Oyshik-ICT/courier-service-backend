from django.urls import path
from .views import CreateStripeCheckoutSession, PaymentSuccessView, PaymentCancelView

urlpatterns = [
    path('order/<uuid:order_id>/', CreateStripeCheckoutSession.as_view(), name='order-pay'),
    path('payment-success/', PaymentSuccessView.as_view(), name="payment-success"),
    path('payment-cancel/', PaymentCancelView.as_view(), name="payment-cancel"),
]

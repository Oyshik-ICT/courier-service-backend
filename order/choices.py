from django.db import models

class StatusChoice(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "Cancelled", "Cancelled"

class PaymentStatusChoice(models.TextChoices):
    PAID = "PAID", "Paid"
    UNPAID = "UNPAID", "Unpaid"
    PAYMENT_PENDING = "PAYMENT_PENDING", "Payment_Pending"

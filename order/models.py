import uuid

from django.db import models

from accounts.models import CustomUser

from .choices import PaymentStatusChoice, StatusChoice


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="send_orders"
    )
    sender_phone = models.CharField(max_length=15)
    pickup_address = models.CharField(max_length=150)
    delivery_address = models.CharField(max_length=150)
    receiver_name = models.CharField(max_length=50)
    receiver_phone = models.CharField(max_length=15)
    package_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField(default=100)
    tracking_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoice.choices, default=StatusChoice.PENDING
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.UNPAID,
    )
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    delivery_man = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="assigned_orders",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = f"TRK{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sender is {self.sender}"

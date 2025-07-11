# Generated by Django 5.2.4 on 2025-07-06 07:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "order_id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("sender_phone", models.CharField(max_length=15)),
                ("pickup_address", models.CharField(max_length=150)),
                ("delivery_address", models.CharField(max_length=150)),
                ("receiver_name", models.CharField(max_length=50)),
                ("receiver_phone", models.CharField(max_length=15)),
                ("package_details", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("price", models.PositiveIntegerField(default=100)),
                (
                    "tracking_number",
                    models.CharField(blank=True, max_length=20, unique=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("CONFIRMED", "Confirmed"),
                            ("DELIVERED", "Delivered"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("PAID", "Paid"),
                            ("UNPAID", "Unpaid"),
                            ("PAYMENT_PENDING", "Payment_Pending"),
                        ],
                        default="UNPAID",
                        max_length=20,
                    ),
                ),
                ("payment_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "delivery_man",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="send_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

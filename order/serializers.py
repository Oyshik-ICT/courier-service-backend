from .models import Order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_id",
            "sender",
            "sender_phone",
            "pickup_address",
            "delivery_address",
            "receiver_name",
            "receiver_phone",
            "package_details",
            "created_at",
            "updated_at",
            "price",
            "tracking_number",
            "status",
            "payment_status",
            "payment_id",
            "delivery_man"
        ]

        extra_kwargs = {
            "order_id": {"read_only": True},
            "sender": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "price": {"read_only": True},
            "tracking_number": {"read_only": True},
            "status": {"read_only": True},
            "payment_status": {"read_only": True},
            "payment_id": {"read_only": True},
            "delivery_man": {"read_only": True},
        }
    
    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)

        return instance


class DeliveryManOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_id",
            "sender_phone",
            "pickup_address",
            "delivery_address",
            "receiver_name",
            "receiver_phone",
            "package_details",
            "created_at",
            "price",
            "tracking_number",
            "status"
        ]

        extra_kwargs = {
            "order_id": {"read_only": True},
            "sender_phone": {"read_only": True},
            "pickup_address": {"read_only": True},
            "delivery_address": {"read_only": True},
            "receiver_name": {"read_only": True},
            "receiver_phone": {"read_only": True},
            "package_details": {"read_only": True},
            "created_at": {"read_only": True},
            "price": {"read_only": True},
            "tracking_number": {"read_only": True},
        }


    
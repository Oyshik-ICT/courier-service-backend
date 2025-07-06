from django.db import models

class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    REGULAR_USER = "REGULAR_USER", "Regular_User"
    DELIVERY_MAN = "DELIVERY_MAN", "Delivery_Man"
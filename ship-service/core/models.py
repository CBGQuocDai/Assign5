from django.db import models


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days_min = models.IntegerField(default=1)
    estimated_days_max = models.IntegerField(default=7)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shipping_method'


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('processing', 'Processing'),
        ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('failed', 'Failed'),
    ]
    order_id = models.IntegerField(unique=True)
    method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    recipient_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment for Order #{self.order_id}"

    class Meta:
        db_table = 'shipment'

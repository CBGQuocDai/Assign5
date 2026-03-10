from django.contrib import admin
from .models import ShippingMethod, Shipment

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'price', 'estimated_days_min', 'estimated_days_max', 'is_active']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'method', 'recipient_name', 'status', 'tracking_number', 'created_at']
    list_filter = ['status']

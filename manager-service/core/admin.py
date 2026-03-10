from django.contrib import admin
from .models import Manager, Coupon

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active', 'created_at']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_to']
    list_filter = ['is_active', 'discount_type']

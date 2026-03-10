from rest_framework import serializers
from .models import Manager, Coupon


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import Manager, Coupon
from .serializers import ManagerSerializer, CouponSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            manager = Manager.objects.get(email=email)
            if check_password(password, manager.password):
                return Response({'status': 'success', 'manager': ManagerSerializer(manager).data})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        order_amount = float(request.data.get('order_amount', 0))
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            now = timezone.now()
            if coupon.valid_from <= now <= coupon.valid_to:
                if order_amount >= float(coupon.min_order_amount):
                    return Response({'valid': True, 'coupon': CouponSerializer(coupon).data})
                return Response({'valid': False, 'error': f'Minimum order amount is {coupon.min_order_amount}'})
            return Response({'valid': False, 'error': 'Coupon has expired'})
        except Coupon.DoesNotExist:
            return Response({'valid': False, 'error': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)

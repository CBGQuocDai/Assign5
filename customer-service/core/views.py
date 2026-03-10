import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        # Auto-create cart for new customer
        try:
            cart_url = getattr(settings, 'CART_SERVICE_URL', 'http://localhost:8006')
            requests.post(f'{cart_url}/api/carts/', json={'customer_id': customer.id}, timeout=3)
        except Exception:
            pass  # Cart creation failure should not block registration
        return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                return Response({'status': 'success', 'customer': CustomerSerializer(customer).data})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

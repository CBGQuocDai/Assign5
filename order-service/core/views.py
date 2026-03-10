import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        items_data = data.pop('items', [])
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Create order items
        for item in items_data:
            item['order'] = order.id
            item_ser = OrderItemSerializer(data=item)
            if item_ser.is_valid():
                item_ser.save()

        # Trigger payment creation
        try:
            pay_url = getattr(settings, 'PAY_SERVICE_URL', 'http://localhost:8009')
            requests.post(f'{pay_url}/api/payments/', json={
                'order_id': order.id,
                'method_code': order.payment_method,
                'amount': str(order.total_amount),
            }, timeout=3)
        except Exception:
            pass

        # Trigger shipment creation
        try:
            ship_url = getattr(settings, 'SHIP_SERVICE_URL', 'http://localhost:8008')
            requests.post(f'{ship_url}/api/shipments/', json={
                'order_id': order.id,
                'method_code': order.shipping_method,
                'address': order.shipping_address,
                'recipient_name': f'Customer {order.customer_id}',
                'phone': '0900000000',
            }, timeout=3)
        except Exception:
            pass

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def by_customer(self, request, customer_id=None):
        orders = Order.objects.filter(customer_id=customer_id)
        return Response(OrderSerializer(orders, many=True).data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

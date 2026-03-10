import uuid
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PaymentMethod, Payment
from .serializers import PaymentMethodSerializer, PaymentSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        method_code = data.pop('method_code', 'cod')
        try:
            method = PaymentMethod.objects.get(code=method_code)
            data['method'] = method.id
        except PaymentMethod.DoesNotExist:
            pass
        data['transaction_id'] = str(uuid.uuid4()).replace('-', '').upper()[:16]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='order/(?P<order_id>[^/.]+)')
    def by_order(self, request, order_id=None):
        try:
            payment = Payment.objects.get(order_id=order_id)
            return Response(PaymentSerializer(payment).data)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'pending':
            return Response({'error': 'Payment already processed'}, status=status.HTTP_400_BAD_REQUEST)
        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.save()
        return Response(PaymentSerializer(payment).data)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'completed':
            return Response({'error': 'Only completed payments can be refunded'}, status=status.HTTP_400_BAD_REQUEST)
        payment.status = 'refunded'
        payment.save()
        return Response(PaymentSerializer(payment).data)

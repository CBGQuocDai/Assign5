import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ShippingMethod, Shipment
from .serializers import ShippingMethodSerializer, ShipmentSerializer


class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        method_code = data.pop('method_code', 'standard')
        try:
            method = ShippingMethod.objects.get(code=method_code)
            data['method'] = method.id
        except ShippingMethod.DoesNotExist:
            pass
        data['tracking_number'] = str(uuid.uuid4()).replace('-', '').upper()[:12]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='order/(?P<order_id>[^/.]+)')
    def by_order(self, request, order_id=None):
        try:
            shipment = Shipment.objects.get(order_id=order_id)
            return Response(ShipmentSerializer(shipment).data)
        except Shipment.DoesNotExist:
            return Response({'error': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Shipment.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        shipment.status = new_status
        shipment.save()
        return Response(ShipmentSerializer(shipment).data)

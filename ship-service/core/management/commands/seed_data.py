from django.core.management.base import BaseCommand
from core.models import ShippingMethod, Shipment


class Command(BaseCommand):
    help = 'Seed shipping methods and shipments'

    def handle(self, *args, **options):
        ShippingMethod.objects.all().delete()
        Shipment.objects.all().delete()

        methods = [
            {'id': 1, 'name': 'Standard Shipping', 'code': 'standard', 'price': 2.99, 'estimated_days_min': 5, 'estimated_days_max': 7},
            {'id': 2, 'name': 'Express Shipping', 'code': 'express', 'price': 9.99, 'estimated_days_min': 2, 'estimated_days_max': 3},
            {'id': 3, 'name': 'Overnight Shipping', 'code': 'overnight', 'price': 19.99, 'estimated_days_min': 1, 'estimated_days_max': 1},
            {'id': 4, 'name': 'Free Shipping', 'code': 'free', 'price': 0, 'estimated_days_min': 7, 'estimated_days_max': 14},
        ]
        for m in methods:
            ShippingMethod.objects.create(**m)

        addresses = [
            '123 Main St, Hanoi', '456 Oak Ave, HCMC', '789 Pine Rd, Da Nang', '321 Elm St, Hue',
            '654 Maple Dr, Can Tho', '987 Cedar Ln, Hai Phong', '147 Birch Blvd, Nha Trang',
            '258 Walnut Way, Vung Tau', '369 Oak St, Bien Hoa', '741 Pine Ave, Thu Duc',
        ]
        names = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Edward Norton',
                 'Fiona Green', 'George Miller', 'Hannah White', 'Ivan Petrov', 'Julia Roberts']
        phones = ['0911111111', '0912222222', '0913333333', '0914444444', '0915555555',
                  '0916666666', '0917777777', '0918888888', '0919999999', '0920000000']
        method_codes = ['standard', 'express', 'standard', 'standard', 'express', 'free', 'overnight', 'standard', 'standard', 'free']
        statuses = ['delivered', 'in_transit', 'processing', 'pending', 'delivered', 'processing', 'in_transit', 'delivered', 'pending', 'processing']

        for i in range(10):
            method = ShippingMethod.objects.get(code=method_codes[i])
            Shipment.objects.create(
                id=i + 1,
                order_id=i + 1,
                method=method,
                recipient_name=names[i],
                address=addresses[i],
                phone=phones[i],
                status=statuses[i],
                tracking_number=f'TRK{str(i+1).zfill(9)}',
            )
        with connection.cursor() as cursor:
            for tbl in ['shipping_method', 'shipment']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 4 shipping methods and 10 shipments'))

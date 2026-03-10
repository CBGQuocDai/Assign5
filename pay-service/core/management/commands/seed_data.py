from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from core.models import PaymentMethod, Payment


class Command(BaseCommand):
    help = 'Seed payment methods and 10 payment records'

    def handle(self, *args, **options):
        PaymentMethod.objects.all().delete()
        Payment.objects.all().delete()

        methods = [
            {'id': 1, 'name': 'Cash on Delivery', 'code': 'cod'},
            {'id': 2, 'name': 'Credit Card', 'code': 'credit_card'},
            {'id': 3, 'name': 'Bank Transfer', 'code': 'bank_transfer'},
            {'id': 4, 'name': 'PayPal', 'code': 'paypal'},
        ]
        for m in methods:
            PaymentMethod.objects.create(**m)

        amounts = [31.98, 18.99, 38.97, 24.99, 39.98, 14.99, 39.99, 27.98, 22.99, 23.98]
        method_codes = ['cod', 'credit_card', 'bank_transfer', 'cod', 'paypal', 'cod', 'credit_card', 'cod', 'bank_transfer', 'cod']
        statuses = ['completed', 'completed', 'completed', 'pending', 'completed', 'completed', 'completed', 'completed', 'pending', 'completed']
        paid_dt = make_aware(datetime(2026, 2, 1))

        for i in range(10):
            method = PaymentMethod.objects.get(code=method_codes[i])
            Payment.objects.create(
                id=i + 1,
                order_id=i + 1,
                method=method,
                amount=amounts[i],
                status=statuses[i],
                transaction_id=f'TXN{str(i+1).zfill(13)}',
                paid_at=paid_dt if statuses[i] == 'completed' else None,
            )
        with connection.cursor() as cursor:
            for tbl in ['payment_method', 'payment']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 4 payment methods and 10 payments'))

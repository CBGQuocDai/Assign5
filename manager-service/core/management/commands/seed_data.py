from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
from datetime import datetime
from core.models import Manager, Coupon


class Command(BaseCommand):
    help = 'Seed 10 manager and 10 coupon records'

    def handle(self, *args, **options):
        Manager.objects.all().delete()
        Coupon.objects.all().delete()
        password = make_password('admin123')
        managers = [
            {'id': 1, 'name': 'Manager One', 'email': 'manager1@bookstore.com'},
            {'id': 2, 'name': 'Manager Two', 'email': 'manager2@bookstore.com'},
            {'id': 3, 'name': 'Manager Three', 'email': 'manager3@bookstore.com'},
            {'id': 4, 'name': 'Manager Four', 'email': 'manager4@bookstore.com'},
            {'id': 5, 'name': 'Manager Five', 'email': 'manager5@bookstore.com'},
            {'id': 6, 'name': 'Manager Six', 'email': 'manager6@bookstore.com'},
            {'id': 7, 'name': 'Manager Seven', 'email': 'manager7@bookstore.com'},
            {'id': 8, 'name': 'Manager Eight', 'email': 'manager8@bookstore.com'},
            {'id': 9, 'name': 'Manager Nine', 'email': 'manager9@bookstore.com'},
            {'id': 10, 'name': 'Manager Ten', 'email': 'manager10@bookstore.com'},
        ]
        for m in managers:
            m['password'] = password
            Manager.objects.create(**m)

        vf = make_aware(datetime(2025, 1, 1))
        vt = make_aware(datetime(2026, 12, 31))
        coupons = [
            {'id': 1, 'code': 'SUMMER10', 'discount_type': 'percent', 'discount_value': 10, 'min_order_amount': 50, 'valid_from': vf, 'valid_to': vt, 'created_by': 1},
            {'id': 2, 'code': 'WINTER20', 'discount_type': 'percent', 'discount_value': 20, 'min_order_amount': 80, 'valid_from': vf, 'valid_to': vt, 'created_by': 1},
            {'id': 3, 'code': 'SPRING15', 'discount_type': 'percent', 'discount_value': 15, 'min_order_amount': 60, 'valid_from': vf, 'valid_to': vt, 'created_by': 2},
            {'id': 4, 'code': 'WELCOME5', 'discount_type': 'percent', 'discount_value': 5, 'min_order_amount': 0, 'valid_from': vf, 'valid_to': vt, 'created_by': 2},
            {'id': 5, 'code': 'FLASH30', 'discount_type': 'percent', 'discount_value': 30, 'min_order_amount': 100, 'valid_from': vf, 'valid_to': vt, 'created_by': 3},
            {'id': 6, 'code': 'BOOK10', 'discount_type': 'fixed', 'discount_value': 10, 'min_order_amount': 50, 'valid_from': vf, 'valid_to': vt, 'created_by': 3},
            {'id': 7, 'code': 'VIP25', 'discount_type': 'percent', 'discount_value': 25, 'min_order_amount': 120, 'valid_from': vf, 'valid_to': vt, 'created_by': 4},
            {'id': 8, 'code': 'STUDENT10', 'discount_type': 'percent', 'discount_value': 10, 'min_order_amount': 30, 'valid_from': vf, 'valid_to': vt, 'created_by': 4},
            {'id': 9, 'code': 'MEMBER15', 'discount_type': 'percent', 'discount_value': 15, 'min_order_amount': 70, 'valid_from': vf, 'valid_to': vt, 'created_by': 5},
            {'id': 10, 'code': 'NEWUSER20', 'discount_type': 'percent', 'discount_value': 20, 'min_order_amount': 0, 'valid_from': vf, 'valid_to': vt, 'created_by': 5},
        ]
        for c in coupons:
            Coupon.objects.create(**c)
        with connection.cursor() as cursor:
            for tbl in ['manager', 'coupon']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 managers and 10 coupons'))

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import connection
from core.models import Customer


class Command(BaseCommand):
    help = 'Seed 10 customer records'

    def handle(self, *args, **options):
        Customer.objects.all().delete()
        password = make_password('customer123')
        customers = [
            {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'phone': '0911111111', 'address': '123 Main St, Hanoi'},
            {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'phone': '0912222222', 'address': '456 Oak Ave, HCMC'},
            {'id': 3, 'name': 'Charlie Brown', 'email': 'charlie@example.com', 'phone': '0913333333', 'address': '789 Pine Rd, Da Nang'},
            {'id': 4, 'name': 'Diana Prince', 'email': 'diana@example.com', 'phone': '0914444444', 'address': '321 Elm St, Hue'},
            {'id': 5, 'name': 'Edward Norton', 'email': 'edward@example.com', 'phone': '0915555555', 'address': '654 Maple Dr, Can Tho'},
            {'id': 6, 'name': 'Fiona Green', 'email': 'fiona@example.com', 'phone': '0916666666', 'address': '987 Cedar Ln, Hai Phong'},
            {'id': 7, 'name': 'George Miller', 'email': 'george@example.com', 'phone': '0917777777', 'address': '147 Birch Blvd, Nha Trang'},
            {'id': 8, 'name': 'Hannah White', 'email': 'hannah@example.com', 'phone': '0918888888', 'address': '258 Walnut Way, Vung Tau'},
            {'id': 9, 'name': 'Ivan Petrov', 'email': 'ivan@example.com', 'phone': '0919999999', 'address': '369 Oak St, Bien Hoa'},
            {'id': 10, 'name': 'Julia Roberts', 'email': 'julia@example.com', 'phone': '0920000000', 'address': '741 Pine Ave, Thu Duc'},
        ]
        for c in customers:
            c['password'] = password
            Customer.objects.create(**c)
        with connection.cursor() as cursor:
            for tbl in ['customer']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 customer records'))

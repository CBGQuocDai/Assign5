from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.hashers import make_password
from core.models import Staff


class Command(BaseCommand):
    help = 'Seed 10 staff records'

    def handle(self, *args, **options):
        Staff.objects.all().delete()
        password = make_password('password123')
        records = [
            {'id': 1, 'name': 'John Admin', 'email': 'john.admin@bookstore.com', 'role': 'supervisor', 'phone': '0901111111'},
            {'id': 2, 'name': 'Jane Supervisor', 'email': 'jane.sup@bookstore.com', 'role': 'senior_staff', 'phone': '0902222222'},
            {'id': 3, 'name': 'Mike Johnson', 'email': 'mike.j@bookstore.com', 'role': 'staff', 'phone': '0903333333'},
            {'id': 4, 'name': 'Sarah Lee', 'email': 'sarah.lee@bookstore.com', 'role': 'staff', 'phone': '0904444444'},
            {'id': 5, 'name': 'David Park', 'email': 'david.park@bookstore.com', 'role': 'staff', 'phone': '0905555555'},
            {'id': 6, 'name': 'Emma Wilson', 'email': 'emma.w@bookstore.com', 'role': 'senior_staff', 'phone': '0906666666'},
            {'id': 7, 'name': 'Chris Brown', 'email': 'chris.b@bookstore.com', 'role': 'staff', 'phone': '0907777777'},
            {'id': 8, 'name': 'Lisa Taylor', 'email': 'lisa.t@bookstore.com', 'role': 'staff', 'phone': '0908888888'},
            {'id': 9, 'name': 'Tom Anderson', 'email': 'tom.a@bookstore.com', 'role': 'staff', 'phone': '0909999999'},
            {'id': 10, 'name': 'Amy Garcia', 'email': 'amy.g@bookstore.com', 'role': 'staff', 'phone': '0910000000'},
        ]
        for r in records:
            r['password'] = password
            Staff.objects.create(**r)
        with connection.cursor() as cursor:
            for tbl in ['staff']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 staff records'))

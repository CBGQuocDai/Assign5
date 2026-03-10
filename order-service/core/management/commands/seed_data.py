from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Seed 10 orders with items'

    def handle(self, *args, **options):
        Order.objects.all().delete()
        book_data = [
            (1, '1984', 15.99), (2, 'Foundation', 18.99), (3, 'Murder on the Orient Express', 12.99),
            (4, 'Steve Jobs', 24.99), (5, 'Sapiens', 19.99), (6, 'How to Win Friends', 14.99),
            (7, 'Clean Code', 39.99), (8, 'The Notebook', 13.99),
            (9, "Harry Potter and the Philosopher's Stone", 22.99), (10, 'Twenty Love Poems', 11.99),
        ]
        qtys = [2, 1, 3, 1, 2, 1, 1, 2, 1, 2]
        addresses = [
            '123 Main St, Hanoi', '456 Oak Ave, HCMC', '789 Pine Rd, Da Nang', '321 Elm St, Hue',
            '654 Maple Dr, Can Tho', '987 Cedar Ln, Hai Phong', '147 Birch Blvd, Nha Trang',
            '258 Walnut Way, Vung Tau', '369 Oak St, Bien Hoa', '741 Pine Ave, Thu Duc',
        ]
        pay_methods = ['cod', 'credit_card', 'bank_transfer', 'cod', 'paypal', 'cod', 'credit_card', 'cod', 'bank_transfer', 'cod']
        ship_methods = ['standard', 'express', 'standard', 'standard', 'express', 'free', 'overnight', 'standard', 'standard', 'free']
        statuses = ['delivered', 'shipped', 'confirmed', 'pending', 'delivered', 'confirmed', 'shipped', 'delivered', 'pending', 'confirmed']
        coupon_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for i in range(10):
            bid, btitle, bprice = book_data[i]
            qty = qtys[i]
            total = round(bprice * qty, 2)
            order = Order.objects.create(
                id=i + 1,
                customer_id=i + 1,
                total_amount=total,
                coupon_id=coupon_ids[i],
                discount_amount=0,
                status=statuses[i],
                payment_method=pay_methods[i],
                shipping_method=ship_methods[i],
                shipping_address=addresses[i],
            )
            OrderItem.objects.create(
                order=order, book_id=bid, book_title=btitle,
                quantity=qty, unit_price=bprice, subtotal=total,
            )
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('order', 'id'), COALESCE((SELECT MAX(id) FROM \"order\"), 1))")
            cursor.execute("SELECT setval(pg_get_serial_sequence('order_item', 'id'), COALESCE((SELECT MAX(id) FROM order_item), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 orders with items'))

from django.core.management.base import BaseCommand
from core.models import Cart, CartItem


class Command(BaseCommand):
    help = 'Seed 10 carts (one per customer) with items'

    def handle(self, *args, **options):
        Cart.objects.all().delete()
        # Seed carts: customer_id 1-10
        for i in range(1, 11):
            Cart.objects.create(id=i, customer_id=i)

        # Seed cart items: each cart has one item
        items = [
            {'cart_id': 1, 'book_id': 1, 'quantity': 2},
            {'cart_id': 2, 'book_id': 2, 'quantity': 1},
            {'cart_id': 3, 'book_id': 3, 'quantity': 3},
            {'cart_id': 4, 'book_id': 4, 'quantity': 1},
            {'cart_id': 5, 'book_id': 5, 'quantity': 2},
            {'cart_id': 6, 'book_id': 6, 'quantity': 1},
            {'cart_id': 7, 'book_id': 7, 'quantity': 1},
            {'cart_id': 8, 'book_id': 8, 'quantity': 2},
            {'cart_id': 9, 'book_id': 9, 'quantity': 1},
            {'cart_id': 10, 'book_id': 10, 'quantity': 2},
        ]
        for it in items:
            cart = Cart.objects.get(id=it['cart_id'])
            CartItem.objects.create(cart=cart, book_id=it['book_id'], quantity=it['quantity'])
        with connection.cursor() as cursor:
            for tbl in ['cart', 'cart_item']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 carts and 10 cart items'))

from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Review


class Command(BaseCommand):
    help = 'Seed 10 review records'

    def handle(self, *args, **options):
        Review.objects.all().delete()
        reviews = [
            {'id': 1, 'customer_id': 1, 'book_id': 1, 'order_id': 1, 'rating': 5, 'comment': 'A masterpiece! 1984 is absolutely terrifying and brilliant.'},
            {'id': 2, 'customer_id': 2, 'book_id': 2, 'order_id': 2, 'rating': 5, 'comment': 'Asimov at his best. Foundation is epic science fiction.'},
            {'id': 3, 'customer_id': 3, 'book_id': 3, 'order_id': 3, 'rating': 4, 'comment': 'Classic Christie mystery with a surprising twist!'},
            {'id': 4, 'customer_id': 4, 'book_id': 4, 'order_id': 4, 'rating': 4, 'comment': 'Fascinating look into the mind of Steve Jobs.'},
            {'id': 5, 'customer_id': 5, 'book_id': 5, 'order_id': 5, 'rating': 5, 'comment': 'Sapiens completely changed how I see human history.'},
            {'id': 6, 'customer_id': 6, 'book_id': 6, 'order_id': 6, 'rating': 4, 'comment': 'Timeless wisdom that still applies today.'},
            {'id': 7, 'customer_id': 7, 'book_id': 7, 'order_id': 7, 'rating': 5, 'comment': 'Essential reading for every software developer.'},
            {'id': 8, 'customer_id': 8, 'book_id': 8, 'order_id': 8, 'rating': 4, 'comment': 'A beautiful and touching love story.'},
            {'id': 9, 'customer_id': 9, 'book_id': 9, 'order_id': 9, 'rating': 5, 'comment': 'Magical! The book that started it all for Harry Potter fans.'},
            {'id': 10, 'customer_id': 10, 'book_id': 10, 'order_id': 10, 'rating': 4, 'comment': "Neruda's poetry is enchanting and deeply moving."},
        ]
        for r in reviews:
            Review.objects.create(**r)
        with connection.cursor() as cursor:
            for tbl in ['review']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 review records'))

from django.core.management.base import BaseCommand
from core.models import Book


class Command(BaseCommand):
    help = 'Seed 10 book records'

    def handle(self, *args, **options):
        Book.objects.all().delete()
        books = [
            {'id': 1, 'title': '1984', 'author_id': 1, 'category_id': 1, 'staff_id': 1, 'price': 15.99, 'stock': 50, 'isbn': '978-0451524935', 'published_date': '1949-06-08', 'description': 'A dystopian novel by George Orwell about a totalitarian society.'},
            {'id': 2, 'title': 'Foundation', 'author_id': 2, 'category_id': 2, 'staff_id': 2, 'price': 18.99, 'stock': 30, 'isbn': '978-0553293357', 'published_date': '1951-05-01', 'description': 'Epic science fiction saga by Isaac Asimov.'},
            {'id': 3, 'title': 'Murder on the Orient Express', 'author_id': 3, 'category_id': 3, 'staff_id': 3, 'price': 12.99, 'stock': 45, 'isbn': '978-0062693662', 'published_date': '1934-01-01', 'description': 'Classic mystery by Agatha Christie featuring Hercule Poirot.'},
            {'id': 4, 'title': 'Steve Jobs', 'author_id': 4, 'category_id': 4, 'staff_id': 4, 'price': 24.99, 'stock': 25, 'isbn': '978-1451648539', 'published_date': '2011-10-24', 'description': 'The exclusive biography of Apple co-founder Steve Jobs.'},
            {'id': 5, 'title': 'Sapiens: A Brief History of Humankind', 'author_id': 5, 'category_id': 5, 'staff_id': 5, 'price': 19.99, 'stock': 60, 'isbn': '978-0062316097', 'published_date': '2011-01-01', 'description': 'Explores the history of the human species by Yuval Harari.'},
            {'id': 6, 'title': 'How to Win Friends and Influence People', 'author_id': 6, 'category_id': 6, 'staff_id': 6, 'price': 14.99, 'stock': 40, 'isbn': '978-0671027032', 'published_date': '1936-10-01', 'description': 'Timeless self-help classic by Dale Carnegie.'},
            {'id': 7, 'title': 'Clean Code', 'author_id': 7, 'category_id': 7, 'staff_id': 7, 'price': 39.99, 'stock': 20, 'isbn': '978-0132350884', 'published_date': '2008-08-01', 'description': 'A handbook of agile software craftsmanship by Robert C. Martin.'},
            {'id': 8, 'title': 'The Notebook', 'author_id': 8, 'category_id': 8, 'staff_id': 8, 'price': 13.99, 'stock': 35, 'isbn': '978-0553528091', 'published_date': '1996-10-01', 'description': 'A romantic love story by Nicholas Sparks.'},
            {'id': 9, 'title': "Harry Potter and the Philosopher's Stone", 'author_id': 9, 'category_id': 9, 'staff_id': 9, 'price': 22.99, 'stock': 55, 'isbn': '978-0439708180', 'published_date': '1997-06-26', 'description': 'The first book in the magical Harry Potter series by J.K. Rowling.'},
            {'id': 10, 'title': 'Twenty Love Poems and a Song of Despair', 'author_id': 10, 'category_id': 10, 'staff_id': 10, 'price': 11.99, 'stock': 30, 'isbn': '978-0140258455', 'published_date': '1924-01-01', 'description': 'Poetry collection by Nobel laureate Pablo Neruda.'},
        ]
        for b in books:
            Book.objects.create(**b)
        with connection.cursor() as cursor:
            for tbl in ['book']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 book records'))

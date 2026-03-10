from django.core.management.base import BaseCommand
from core.models import Category, Author


class Command(BaseCommand):
    help = 'Seed 10 categories and 10 authors'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Author.objects.all().delete()

        categories = [
            {'id': 1, 'name': 'Fiction', 'description': 'Literary fiction and novels'},
            {'id': 2, 'name': 'Science Fiction', 'description': 'Sci-fi and speculative fiction'},
            {'id': 3, 'name': 'Mystery & Thriller', 'description': 'Mystery and suspense books'},
            {'id': 4, 'name': 'Biography', 'description': 'Biographies and memoirs'},
            {'id': 5, 'name': 'History', 'description': 'Historical non-fiction'},
            {'id': 6, 'name': 'Self-Help', 'description': 'Personal development books'},
            {'id': 7, 'name': 'Technology', 'description': 'Programming and tech books'},
            {'id': 8, 'name': 'Romance', 'description': 'Love stories and romance novels'},
            {'id': 9, 'name': "Children's Books", 'description': 'Books for young readers'},
            {'id': 10, 'name': 'Poetry', 'description': 'Poetry collections'},
        ]
        for c in categories:
            Category.objects.create(**c)

        authors = [
            {'id': 1, 'name': 'George Orwell', 'bio': 'English novelist and essayist', 'nationality': 'British'},
            {'id': 2, 'name': 'Isaac Asimov', 'bio': 'American author of science fiction', 'nationality': 'American'},
            {'id': 3, 'name': 'Agatha Christie', 'bio': 'Queen of Crime mystery writer', 'nationality': 'British'},
            {'id': 4, 'name': 'Walter Isaacson', 'bio': 'American author and journalist', 'nationality': 'American'},
            {'id': 5, 'name': 'Yuval Noah Harari', 'bio': 'Israeli historian and author', 'nationality': 'Israeli'},
            {'id': 6, 'name': 'Dale Carnegie', 'bio': 'American writer and lecturer', 'nationality': 'American'},
            {'id': 7, 'name': 'Robert C. Martin', 'bio': 'Software engineer and author', 'nationality': 'American'},
            {'id': 8, 'name': 'Nicholas Sparks', 'bio': 'American romance novelist', 'nationality': 'American'},
            {'id': 9, 'name': 'J.K. Rowling', 'bio': 'British author of Harry Potter series', 'nationality': 'British'},
            {'id': 10, 'name': 'Pablo Neruda', 'bio': 'Chilean poet and diplomat', 'nationality': 'Chilean'},
        ]
        for a in authors:
            Author.objects.create(**a)

        with connection.cursor() as cursor:
            for tbl in ['category', 'author']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 categories and 10 authors'))

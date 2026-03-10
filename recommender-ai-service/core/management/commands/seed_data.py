from django.core.management.base import BaseCommand
from core.models import UserBookInteraction, BookSimilarity


class Command(BaseCommand):
    help = 'Seed recommender interactions and book similarities'

    def handle(self, *args, **options):
        UserBookInteraction.objects.all().delete()
        BookSimilarity.objects.all().delete()

        # Interactions: customers 1-10 purchased books 1-10 (matching orders)
        interactions = [
            {'id': 1, 'customer_id': 1, 'book_id': 1, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 2, 'customer_id': 2, 'book_id': 2, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 3, 'customer_id': 3, 'book_id': 3, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 4, 'customer_id': 4, 'book_id': 4, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 5, 'customer_id': 5, 'book_id': 5, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 6, 'customer_id': 6, 'book_id': 6, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 7, 'customer_id': 7, 'book_id': 7, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 8, 'customer_id': 8, 'book_id': 8, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 9, 'customer_id': 9, 'book_id': 9, 'interaction_type': 'purchase', 'score': 5.0},
            {'id': 10, 'customer_id': 10, 'book_id': 10, 'interaction_type': 'purchase', 'score': 5.0},
        ]
        for it in interactions:
            UserBookInteraction.objects.create(**it)

        # Book similarities: books in same category are similar
        # Category 1 (Fiction): book 1
        # Category 2 (Sci-Fi): book 2
        # Self-help/practical: books 6,7 similar
        # Stories/fiction: books 1,8 similar
        similarities = [
            {'id': 1, 'book_id': 1, 'similar_book_id': 8, 'similarity_score': 0.75, 'category_id': 1},   # fiction
            {'id': 2, 'book_id': 8, 'similar_book_id': 1, 'similarity_score': 0.75, 'category_id': 1},
            {'id': 3, 'book_id': 6, 'similar_book_id': 7, 'similarity_score': 0.70, 'category_id': 6},   # self-help/tech
            {'id': 4, 'book_id': 7, 'similar_book_id': 6, 'similarity_score': 0.70, 'category_id': 7},
            {'id': 5, 'book_id': 4, 'similar_book_id': 5, 'similarity_score': 0.65, 'category_id': 4},   # non-fiction
            {'id': 6, 'book_id': 5, 'similar_book_id': 4, 'similarity_score': 0.65, 'category_id': 5},
            {'id': 7, 'book_id': 2, 'similar_book_id': 3, 'similarity_score': 0.55, 'category_id': 2},   # genre fiction
            {'id': 8, 'book_id': 3, 'similar_book_id': 2, 'similarity_score': 0.55, 'category_id': 3},
            {'id': 9, 'book_id': 9, 'similar_book_id': 10, 'similarity_score': 0.60, 'category_id': 9},  # popular books
            {'id': 10, 'book_id': 10, 'similar_book_id': 9, 'similarity_score': 0.60, 'category_id': 10},
        ]
        for s in similarities:
            BookSimilarity.objects.create(**s)

        with connection.cursor() as cursor:
            for tbl in ['user_book_interaction', 'book_similarity']:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{tbl}', 'id'), COALESCE((SELECT MAX(id) FROM \"{tbl}\"), 1))")
        self.stdout.write(self.style.SUCCESS('Seeded 10 interactions and 10 book similarities'))

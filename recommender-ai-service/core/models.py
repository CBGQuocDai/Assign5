from django.db import models


class UserBookInteraction(models.Model):
    """Tracks customer interactions with books for collaborative filtering."""
    INTERACTION_TYPES = [
        ('view', 'View'), ('purchase', 'Purchase'), ('wishlist', 'Wishlist'), ('review', 'Review'),
    ]
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    score = models.FloatField(default=1.0)  # weight: purchase=5, review=4, wishlist=3, view=1
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_book_interaction'


class BookSimilarity(models.Model):
    """Pre-computed book similarity scores (content-based)."""
    book_id = models.IntegerField()
    similar_book_id = models.IntegerField()
    similarity_score = models.FloatField()
    category_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'book_similarity'
        unique_together = ('book_id', 'similar_book_id')

from django.contrib import admin
from .models import UserBookInteraction, BookSimilarity

@admin.register(UserBookInteraction)
class UserBookInteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'book_id', 'interaction_type', 'score', 'created_at']

@admin.register(BookSimilarity)
class BookSimilarityAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_id', 'similar_book_id', 'similarity_score', 'category_id']

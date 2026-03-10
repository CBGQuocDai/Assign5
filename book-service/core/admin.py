from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author_id', 'category_id', 'price', 'stock', 'created_at']
    list_filter = ['category_id']
    search_fields = ['title', 'isbn']

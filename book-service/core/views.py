from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.all()
        category = self.request.query_params.get('category_id')
        author = self.request.query_params.get('author_id')
        staff = self.request.query_params.get('staff_id')
        if category:
            qs = qs.filter(category_id=category)
        if author:
            qs = qs.filter(author_id=author)
        if staff:
            qs = qs.filter(staff_id=staff)
        return qs

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        books = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return Response(BookSerializer(books, many=True).data)

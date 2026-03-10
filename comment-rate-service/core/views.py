from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=['get'], url_path='book/(?P<book_id>[^/.]+)')
    def by_book(self, request, book_id=None):
        reviews = Review.objects.filter(book_id=book_id, is_approved=True)
        avg = reviews.aggregate(avg_rating=Avg('rating'))
        return Response({
            'book_id': book_id,
            'average_rating': round(avg['avg_rating'] or 0, 2),
            'total_reviews': reviews.count(),
            'reviews': ReviewSerializer(reviews, many=True).data,
        })

    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def by_customer(self, request, customer_id=None):
        reviews = Review.objects.filter(customer_id=customer_id)
        return Response(ReviewSerializer(reviews, many=True).data)

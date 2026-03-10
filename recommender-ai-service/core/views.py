import requests
from collections import defaultdict
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import UserBookInteraction, BookSimilarity
from .serializers import UserBookInteractionSerializer, BookSimilaritySerializer


class UserBookInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserBookInteraction.objects.all()
    serializer_class = UserBookInteractionSerializer


class BookSimilarityViewSet(viewsets.ModelViewSet):
    queryset = BookSimilarity.objects.all()
    serializer_class = BookSimilaritySerializer


@api_view(['GET'])
def recommend_for_customer(request, customer_id):
    """
    Hybrid recommendation:
    1. Collaborative: find books purchased/reviewed by similar customers
    2. Content-based: use BookSimilarity for books the customer interacted with
    """
    # Books the customer already interacted with
    my_interactions = UserBookInteraction.objects.filter(customer_id=customer_id)
    my_book_ids = set(my_interactions.values_list('book_id', flat=True))

    scores = defaultdict(float)

    # Content-based: similar books to what customer interacted with
    for book_id in my_book_ids:
        for sim in BookSimilarity.objects.filter(book_id=book_id).order_by('-similarity_score')[:5]:
            if sim.similar_book_id not in my_book_ids:
                scores[sim.similar_book_id] += sim.similarity_score

    # Collaborative: other customers who share purchases
    if my_book_ids:
        similar_customers = UserBookInteraction.objects.filter(
            book_id__in=my_book_ids, interaction_type='purchase'
        ).values_list('customer_id', flat=True).distinct()

        for other_customer_id in similar_customers:
            if str(other_customer_id) == str(customer_id):
                continue
            for interaction in UserBookInteraction.objects.filter(
                customer_id=other_customer_id, interaction_type='purchase'
            ):
                if interaction.book_id not in my_book_ids:
                    scores[interaction.book_id] += interaction.score * 0.5

    # Sort by score
    sorted_books = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    recommended_book_ids = [bid for bid, _ in sorted_books]

    # Fetch book details from book-service
    book_details = []
    book_service_url = getattr(settings, 'BOOK_SERVICE_URL', 'http://localhost:8005')
    for book_id in recommended_book_ids:
        try:
            resp = requests.get(f'{book_service_url}/api/books/{book_id}/', timeout=2)
            if resp.status_code == 200:
                book_details.append(resp.json())
        except Exception:
            book_details.append({'id': book_id})

    return Response({
        'customer_id': customer_id,
        'recommended_books': book_details,
    })


@api_view(['GET'])
def similar_books(request, book_id):
    """Return books similar to a given book."""
    sims = BookSimilarity.objects.filter(book_id=book_id).order_by('-similarity_score')[:10]
    return Response(BookSimilaritySerializer(sims, many=True).data)

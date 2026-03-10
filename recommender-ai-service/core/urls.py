from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserBookInteractionViewSet, BookSimilarityViewSet, recommend_for_customer, similar_books

router = DefaultRouter()
router.register(r'interactions', UserBookInteractionViewSet)
router.register(r'similarities', BookSimilarityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommend/customer/<int:customer_id>/', recommend_for_customer),
    path('recommend/similar/<int:book_id>/', similar_books),
]

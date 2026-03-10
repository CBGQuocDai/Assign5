from rest_framework import serializers
from .models import UserBookInteraction, BookSimilarity


class UserBookInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookInteraction
        fields = '__all__'


class BookSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSimilarity
        fields = '__all__'

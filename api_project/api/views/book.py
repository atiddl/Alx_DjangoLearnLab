from rest_framework import generics
from api.models import Book
from api.serializers.book import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

# BookListView:
# - Provides read-only access to all book entries.
# - Publicly accessible using ListAPIView.

# BookCreateView:
# - Allows authenticated users to create new books.
# - Uses built-in CreateAPIView and custom validation in serializer.

# BookUpdateView / BookDeleteView:
# - Modify or delete existing books by ID.
# - Access restricted to authenticated users via IsAuthenticated permission.


from django_filters import rest_framework

class BookListView(generics.ListAPIView):
    """
    List all books with support for filtering, searching, and ordering.

    Query Parameters:
    - Filtering:
      ?title=some_title
      ?author=1  (author ID)
      ?publication_year=2024

    - Search:
      ?search=1984 (matches title or author name)

    - Ordering:
      ?ordering=title
      ?ordering=-publication_year (descending)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']


# class BookListView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [permissions.IsAuthenticated]  

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admin users can create/update/delete
            permission_classes = [permissions.IsAdminUser]
        else:
            # Other actions only require authentication
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


"""
BookViewSet Permissions:

- Read operations require authentication.
- Create, Update, and Delete operations require admin privileges.
"""

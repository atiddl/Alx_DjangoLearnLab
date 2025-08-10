from rest_framework import serializers
from .models import Author, Book
import datetime

"""
Serializers:
BookSerializer - serializes all book fields and validates publication year.
AuthorSerializer - serializes author's name and includes a nested list of books using BookSerializer.
"""

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  

    class Meta:
        model = Author
        fields = ['name', 'books']

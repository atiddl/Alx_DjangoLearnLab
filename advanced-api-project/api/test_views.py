from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test authors and books
        self.author1 = Author.objects.create(name="Author One")
        self.book1 = Book.objects.create(title="Book One", publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2010, author=self.author1)
        
        # API client
        self.client = APIClient()
        
        # URLs
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})

    def test_list_books(self):
        # Unauthenticated users can list books
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # two books created

    def test_retrieve_book_detail(self):
        response = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Book One")

    def test_create_book_requires_authentication(self):
        data = {
            'title': "New Book",
            'publication_year': 2021,
            'author': self.author1.pk
        }
        # Without login
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # With login
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': "Updated Title",
            'publication_year': 2005,
            'author': self.author1.pk
        }
        response = self.client.put(self.update_url(self.book1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url(self.book2.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure book is deleted
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {'title': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books_by_author_name(self):
        response = self.client.get(self.list_url, {'search': 'Author One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books_by_publication_year(self):
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_public_read_only_access(self):
        # Unauthenticated users cannot create, update, or delete
        data = {
            'title': "Unauthorized Create",
            'publication_year': 2025,
            'author': self.author1.pk
        }
        create_response = self.client.post(self.create_url, data)
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        update_response = self.client.put(self.update_url(self.book1.pk), data)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        delete_response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

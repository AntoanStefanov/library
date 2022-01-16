from books.views import (AboutView, BookCreateView, BookDeleteView,
                         BookDetailsView, BookListView, BookUpdateView,
                         HomeView, MyBookListView)
from django.test import TestCase
from django.urls import resolve, reverse


class TestUrls(TestCase):
    """ Reverse an URL and resolve that URL to see which view Django calls.
        Check status code returned from responses.
    """
    
    def test_books_about_url_is_resolved(self):
        url = reverse('books_about')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, AboutView)

    def test_books_create_url_is_resolved(self):
        url = reverse('books_create')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, BookCreateView)

    def test_books_delete_url_is_resolved(self):
        url = reverse('books_delete',  kwargs={'pk': 3})
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, BookDeleteView)

    def test_book_details_url_is_resolved(self):
        url = reverse('book_details',  kwargs={'pk': 3})
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, BookDetailsView)

    def test_books_library_url_is_resolved(self):
        url = reverse('books_library')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, BookListView)

    def test_books_update_url_is_resolved(self):
        url = reverse('books_update', kwargs={'pk': 3})
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, BookUpdateView)

    def test_books_home_url_is_resolved(self):
        url = reverse('books_home')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, HomeView)


    def test_my_books_url_is_resolved(self):
        url = reverse('my_books')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, MyBookListView)
        
    def test_books_about_url_response(self):
        response = self.client.get(reverse('books_about'))
        self.assertEqual(response.status_code, 200)

    def test_books_create_url_response(self):
        """
            Redirection code - 302. User not logged in.
        """
        response = self.client.get(reverse('books_create'))
        self.assertEqual(response.status_code, 302)
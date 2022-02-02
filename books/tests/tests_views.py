from books.models import Book
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class TestBooksViews(TestCase):
    """
        All the tests in this module use the client (belonging to our TestCase's derived class).
    """

    @classmethod
    def setUpTestData(cls):
        """ 
            Set up data for the whole TestCase.
            https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.TestCase.setUpTestData

        """

        # https://stackoverflow.com/questions/63054997/difference-between-user-objects-create-user-vs-user-objects-create-vs-user
        cls.user = User.objects.create_user(
            username='testuser', password='12345')

        cls.book = Book.objects.create(
            title="Title",
            author="Author",
            language="Bulgarian",
            genre="Comedy",
            description="Description",
            image='default_book.jpg',
            date_posted=timezone.now(),
            posted_by=cls.user
        )

    def setUp(self):
        """
            This function runs before every single test method.
        """

        self.my_books_url = reverse('my_books')
        self.books_create_url = reverse('books_create')
        self.books_update_url = reverse('books_update', kwargs={
            'pk': 2, 'slug': 'title-author'})

    def test_book_list_view(self):
        """
            GET method.
            No login required.
            200 response code.
            Using correct template.
        """
        response = self.client.get(reverse('books_library'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_author_book_list_view(self):
        """
            GET method.
            No login required.
            200 response code.
            Using correct template.
        """
        response = self.client.get(reverse(
            'author_books', kwargs={'author': self.book.author}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_my_book_list_view_not_logged_in(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.my_books_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_list.html')

    def test_my_book_list_view_logged_in(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        # logged_in =
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.my_books_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_books_create_view_not_logged_in(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.books_create_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_form.html')

    def test_books_create_view_logged_in(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.books_create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')

    def test_books_details_view(self):
        """
            GET method.
            No login required.
            200 response code.
            Using correct template.
        """

        response = self.client.get(reverse('books_details', kwargs={
            'pk': 2, 'slug': 'title-author'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_details.html')

    def test_books_update_view_not_logged_in(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.books_update_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_form.html')

    def test_books_update_view_logged_in(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.books_update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')

    # BookDeleteView NEXT

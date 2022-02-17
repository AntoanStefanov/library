from books.models import Book, Comment
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class TestBooksViews(TestCase):
    """
        All the tests in this module use the client (belonging to our TestCase's derived class).
        If test TestCase is runned independently, pk:2 in setUp urls will throw Fails,
        Because in tests_urls.py is creating a book first.
        So here a second book is being created. And if this is run with
        command 'python manage.py test books/tests/tests_views.py' will throw error, because
        then will become the first book('tests_urls.py' has not been run).
        That's why run all tests together, not independently

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
        self.books_details_url = reverse('books_details', kwargs={
            'pk': 2, 'slug': 'title-author'})
        self.profile_favourites = reverse('profile_favourites')
        self.recommended_books = reverse('recommended_books')
        self.genre_books = reverse('genre_books', kwargs={'genre': 'ART'})
        self.profile_books = reverse('profile_books', kwargs={'profile': 'testuser'})

    def test_book_list_view_GET(self):
        """
            GET method.
            No login required.
            200 response code.
            Using correct template.
        """
        response = self.client.get(reverse('books_library'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_favourites_view_not_logged_in_GET(self):
        response = self.client.get(self.profile_favourites)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_list.html')

    def test_favourites_view_logged_in_GET(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        # logged_in =
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.profile_favourites)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_recommended_book_list_view_not_logged_in_GET(self):
        response = self.client.get(self.recommended_books)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_list.html')

    def test_recommended_book_list_view_logged_in_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.recommended_books)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/recommended_book_list.html')

    def test_genre_book_list_view_not_logged_in_GET(self):
        response = self.client.get(self.genre_books)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_list.html')

    def test_genre_book_list_view_logged_in_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.genre_books)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_author_book_list_view_GET(self):
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

    def test_profile_book_list_view_not_logged_in_GET(self):
        response = self.client.get(self.profile_books)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_list.html')

    def test_profile_book_list_view_logged_in_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.profile_books)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_my_book_list_view_not_logged_in_GET(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.my_books_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_list.html')

    def test_my_book_list_view_logged_in_GET(self):
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

    def test_books_create_view_not_logged_in_GET(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.books_create_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_form.html')

    def test_books_create_view_logged_in_GET(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.books_create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')

    def test_books_create_view_logged_in_POST(self):
        """
            Only logged_in POST, because if you are not logged in,
            You will get redirected to login(LoginRequiredMixin),
            already tested(test: test_books_create_view_not_logged_in_GET).
        """
        self.client.login(username='testuser', password='12345')
        data = {
            'title': 'test title',
            'author': 'test author',
            'language': 'test language',
            'genre': 'ART',
            'description': 'test description'
        }

        response = self.client.post(self.books_create_url, data)
        
        # REDIRECT to absolute url in Book model.
        self.assertEqual(response.status_code, 302)
        # assert that user object is added correctly within the form.
        self.assertEqual(Book.objects.all()[1].posted_by, self.user)

    def test_books_details_view_GET(self):
        """
            GET method.
            No login required.
            200 response code.
            Using correct template.
        """

        response = self.client.get(self.books_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_details.html')

    def test_books_details_view_POST(self):
        """
            Test posting comment in view.
        """
        self.client.login(username='testuser', password='12345')
        data = {
            'content': 'test comment',
        }

        response = self.client.post(self.books_details_url, data)

        # REDIRECT to absolute url in Book model, check form_valid method in view.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.all()[0].content, 'test comment')

    def test_books_update_view_not_logged_in_GET(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.books_update_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_form.html')

    def test_books_update_view_logged_in_GET(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.books_update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')

    # TODO update view logged in , POST - edit a book

    # BookDeleteView NEXT

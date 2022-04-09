from books.models import Author, Book, Comment
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class TestBookViews(TestCase):
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

        cls.author = Author.objects.create(
            first_name='Gordon',
            last_name='Ramsay',
            image='https://upload.wikimedia.org/wikipedia/commons/5/5c/JSJoseSaramago.jpg',
            birth_date='2022-03-09',
            biography='Biography'
        )

        cls.author_two = Author.objects.create(
            first_name='Acho',
            last_name='Achev',
            image='https://upload.wikimedia.org/wikipedia/commons/5/5c/JSJoseSaramago.jpg',
            birth_date='2022-03-09',
            biography='Biography'
        )

        cls.book = Book.objects.create(
            title="Title",
            author=cls.author,
            language="Bulgarian",
            genre="COMEDY",
            description="Description",
            date_posted=timezone.now(),
            posted_by=cls.user
        )

    def setUp(self):
        """
            This function runs before every single test method.
            PK:2 , because in test_views, the first book was created,
            setUpTestData class method(above), deletes books from other TestCases(modules).
        """
        BOOK_KWARGS = {'pk': 3, 'slug': 'title-author'}

        self.my_books_url = reverse('my_books')
        self.books_create_url = reverse('books_create')
        self.recommended_books = reverse('recommended_books')
        self.profile_favourites = reverse('profile_favourites')
        self.genre_books = reverse(
            'genre_books',
            kwargs={'genre': 'ART'}
        )
        self.profile_books = reverse(
            'profile_books',
            kwargs={'profile': 'testuser'}
        )
        self.books_update_url = reverse(
            'books_update',
            kwargs=BOOK_KWARGS
        )
        self.books_details_url = reverse(
            'books_details',
            kwargs=BOOK_KWARGS
        )
        self.books_delete_url = reverse(
            'books_delete',
            kwargs=BOOK_KWARGS
        )

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
            'author_books', kwargs={'pk':self.book.author.id, 'author': self.book.author}))

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

    def test_books_create_view_logged_in_POST_book_NO_data(self):
        """
           There is already one book in DB, books count should be 1.
           Book should not be added without data.
           REDIRECT to same form(url).
        """
        self.client.login(username='testuser', password='12345')

        response = self.client.post(self.books_create_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_books_create_view_logged_in_POST_book(self):
        """
            Only logged_in POST, because if you are not logged in,
            You will get redirected to login(LoginRequiredMixin),
            already tested(test: test_books_create_view_not_logged_in_GET).
        """
        self.client.login(username='testuser', password='12345')
        author_pk = self.author.pk
        data = {
            'title': 'test title',
            'author': author_pk,
            'language': 'test language',
            'genre': 'ART',
            'description': 'test description'
        }

        response = self.client.post(self.books_create_url, data)
        books = Book.objects.all()

        # REDIRECT to absolute url in Book model.
        self.assertEqual(response.status_code, 302)
        # assert that user object is added correctly within the form.
        self.assertEqual(books[0].posted_by, self.user)
        self.assertEqual(books[0].title, 'test title')

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

    def test_books_details_view_logged_in_POST_comment_NO_data(self):
        """
            Comment with no data, should not be posted,
            redirect to same url.
        """
        self.client.login(username='testuser', password='12345')

        response = self.client.post(self.books_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_books_details_view_logged_in_POST_comment(self):
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

    def test_books_update_view_logged_in_POST_edit_book_NO_data(self):
        """
            Redirect to same url, book with no data is not edited.
        """

        self.client.login(username='testuser', password='12345')

        response = self.client.post(self.books_update_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.all()[0].title, 'Title')

    def test_books_update_view_logged_in_POST_edit_book(self):

        self.client.login(username='testuser', password='12345')
        author_pk = self.author.pk

        data = {
            'title': 'Title Updated',
            'author': author_pk,
            'language': 'Bulgarian Updated',
            'genre': 'COMEDY',
            'description': 'Description Updated'
        }

        response = self.client.post(self.books_update_url, data)

        # Redirect to book absolute url.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all()[0].posted_by, self.user)
        self.assertEqual(Book.objects.all()[0].title, 'Title Updated')

    def test_books_delete_view_not_logged_in_GET(self):
        """
            GET method.
            302 response code - User not logged in, redirect to login page.
            Not using given template.
        """

        response = self.client.get(self.books_delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books/book_confirm_delete.html')

    def test_books_delete_view_logged_in_GET(self):
        """
            GET method.
            200 response code - User logged in.
            Using given template.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.books_delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_confirm_delete.html')

    def test_books_delete_view_logged_in_POST(self):
        """
            Delete book from db, POST method.
            Redirect to url named 'my books'.
            Book is deleted with no data.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.books_delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)

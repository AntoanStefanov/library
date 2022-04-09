from books.models import Author, Book, Comment
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


class TestBookModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ 
            Set up data for the whole TestCase.
            https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.TestCase.setUpTestData

        """

        cls.user = User.objects.create_user(
            username='testuser',
            password='12345')

        cls.author = Author.objects.create(
            first_name='Gordon',
            last_name='Ramsay',
            image='https://upload.wikimedia.org/wikipedia/commons/5/5c/JSJoseSaramago.jpg',
            birth_date='2022-03-09',
            biography='Biography'
        )

        cls.book = Book.objects.create(
            title="Title test",
            author=cls.author,
            language="Bulgarian",
            genre="COMEDY",
            description="Description",
            date_posted=timezone.now(),
            posted_by=cls.user
        )

    def test_book_is_assigned_slug_on_creation(self):
        self.assertEqual(self.book.slug, 'title-test-gordon-ramsay')

    def test_get_absolute_url(self):
        self.assertEqual(
            self.book.get_absolute_url(),
            '/books/book/1/title-test-gordon-ramsay/'
        )

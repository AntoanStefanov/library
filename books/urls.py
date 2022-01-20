from django.urls import include, path

from .views import (AboutView, BookCreateView, BookDeleteView, BookDetailsView,
                    BookListView, BookUpdateView, HomeView, MyBookListView)

urlpatterns = [
    path('', HomeView.as_view(), name='books_home'),
    path('library/', BookListView.as_view(), name='books_library'),
    path('my-books/', MyBookListView.as_view(), name='my_books'),
    path('about/', AboutView.as_view(), name='books_about'),
    path('book/new/', BookCreateView.as_view(), name='books_create'),
    # https://docs.djangoproject.com/en/4.0/topics/http/urls/#including-other-urlconfs -> ctrl + F -> slug.
    # https://stackoverflow.com/questions/50321644/django-not-matching-unicode-in-url
    # https://docs.djangoproject.com/en/4.0/topics/http/urls/#path-converters
    # str converter does not count space in title/author.
    path('book/<int:pk>/<slug:slug>/', include([
        path('', BookDetailsView.as_view(
            template_name='books/book_details.html'),
            name='book_details'),
        path('update/', BookUpdateView.as_view(), name='books_update'),
        path('delete/', BookDeleteView.as_view(), name='books_delete')
    ]))
]

# as_view() -> Returns a callable view that takes a request and returns a response

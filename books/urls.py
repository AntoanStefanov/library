from django.urls import include, path

from .views import (AuthorBookListView, BookCreateView, BookDeleteView,
                    BookDetailsView, BookListView, BookUpdateView,
                    CommentDeleteView, FavouritesView, GenreBookListView,
                    MyBookListView, ProfileBookListView,
                    RecommendedBookListView)

urlpatterns = [
    path('library/', BookListView.as_view(), name='books_library'),
    path('my-books/', MyBookListView.as_view(), name='my_books'),
    path('recommended/', RecommendedBookListView.as_view(),
         name='recommended_books'),
    path('favourites/', FavouritesView.as_view(), name='profile_favourites'),
    path('<str:profile>-books/', ProfileBookListView.as_view(), name='profile_books'),
    path('<int:pk>/<str:author>/books/', AuthorBookListView.as_view(), name='author_books'),
    path('<str:genre>/', GenreBookListView.as_view(), name='genre_books'),
    path('book/new/', BookCreateView.as_view(), name='books_create'),
    # https://docs.djangoproject.com/en/4.0/topics/http/urls/#including-other-urlconfs -> ctrl + F -> slug.
    # https://stackoverflow.com/questions/50321644/django-not-matching-unicode-in-url
    # https://docs.djangoproject.com/en/4.0/topics/http/urls/#path-converters
    # str converter does not count space in title/author.
    path('book/<int:pk>/<slug:slug>/', include([
        path('', BookDetailsView.as_view(), name='books_details'),
        path('update/', BookUpdateView.as_view(), name='books_update'),
        path('delete/', BookDeleteView.as_view(), name='books_delete'),
        path('comment/<int:id>/update/', BookDetailsView.as_view(),
             name='books_comment_update'),
        path('comment/<int:id>/delete/', CommentDeleteView.as_view(),
             name='books_comment_delete'),
    ]))
]

# as_view() -> Returns a callable view that takes a request and returns a response

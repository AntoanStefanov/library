from django.urls import path
from .views import HomeView, AboutView, BookListView, BookCreateView, BookDetailsView, MyBookListView


urlpatterns = [
    path('', HomeView.as_view(), name='books_home'),
    path('library/', BookListView.as_view(), name='books_library'),
    path('my-books/', MyBookListView.as_view(), name='my_books'),
    path('about/', AboutView.as_view(), name='books_about'),
    path('book/new/', BookCreateView.as_view(), name='books_create'),
    path('book/<int:pk>/', BookDetailsView.as_view(
        template_name='books/book_details.html'), name='book_details'),


]

# as_view() -> Returns a callable view that takes a request and returns a response

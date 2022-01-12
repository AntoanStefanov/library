from django.urls import path
from .views import HomeView, AboutView, BookListView, BookCreateView


urlpatterns = [
    path('', HomeView.as_view(), name='books_home'),
    path('library/', BookListView.as_view(), name='books_library'),
    path('about/', AboutView.as_view(), name='books_about'),
    path('book/new/', BookCreateView.as_view(), name='books_create'),

]

# as_view() -> Returns a callable view that takes a request and returns a response
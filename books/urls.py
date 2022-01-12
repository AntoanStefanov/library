from django.urls import path
from .views import HomeView, AboutView, BookListView


urlpatterns = [
    path('', HomeView.as_view(), name='books_home'),
    path('library/', BookListView.as_view(), name='books_library'),
    path('about/', AboutView.as_view(), name='books_about'),
]

# as_view() -> Returns a callable view that takes a request and returns a response
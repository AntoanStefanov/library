from django.urls import path
from .views import HomeView, BookListView


urlpatterns = [
    path('', HomeView.as_view(), name='books_home'),
    path('library/', BookListView.as_view(), name='books_library'),
]

# as_view() -> Returns a callable view that takes a request and returns a response
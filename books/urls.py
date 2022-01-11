from django.urls import path
from .views import BookListView


urlpatterns = [
    path('', BookListView.as_view(), name='books_home'),
]

# as_view() -> Returns a callable view that takes a request and returns a response
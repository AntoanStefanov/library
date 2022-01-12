from django.views.generic import TemplateView, ListView

from .models import Book


class HomeView(TemplateView):
    template_name = 'books/home.html'


class AboutView(TemplateView):
    template_name = 'books/about.html'


class BookListView(ListView):
    model = Book
    template_name = 'books/library.html'
    ordering = ['-date_posted']
    # change object_list variable
    context_object_name = 'books'

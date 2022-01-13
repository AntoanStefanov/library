from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView

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

class MyBookListView(LoginRequiredMixin, BookListView):
    template_name = 'books/my_books.html'

    def get_queryset(self):
        # ordered here, because the inherited ordering variable does not work. for this class.
        # ordering variable in BookListView class == '-date_posted' in .order_by('-date_posted')
        user_books = Book.objects.filter(posted_by=self.request.user.pk).order_by('-date_posted')
        return user_books


class BookCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin -> IF NOT LOGGED USER TRIES TO CREATE A BOOK - redirect to LOGIN_URL ! 
    # LOGIN_URL = 'login' (path func - name)
    model = Book
    fields = ['title', 'author', 'description', 'image']
    template_name = 'books/create_book.html'

    def form_valid(self, form):
        # take the form instance before submitting
        # and set the user who posted it to the current logged in user
        form.instance.posted_by = self.request.user
        # now validate the form
        return super().form_valid(form)


class BookDetailsView(DetailView):
    model = Book

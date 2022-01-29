from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from library_project.utils import is_user_admin_or_book_owner

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    # change object_list variable for template use
    context_object_name = 'books'
    # pagination
    paginate_by = 2

class UserBookListView(BookListView):
     def get_queryset(self):
        author = self.kwargs.get('author')
        author_books = Book.objects.filter(
            author=author)
        return author_books

class MyBookListView(LoginRequiredMixin, BookListView):

    def get_queryset(self):
        user_books = Book.objects.filter(
            posted_by=self.request.user.pk)
        return user_books


class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # LoginRequiredMixin -> IF NOT LOGGED USER TRIES TO CREATE A BOOK - redirect to LOGIN_URL !
    # LOGIN_URL = 'login' (path func - name)
    model = Book
    fields = ['title', 'author', 'language', 'genre', 'description', 'image']
    success_message = 'Book "%(title)s" was created successfully!'

    def form_valid(self, form):
        # take the form instance before submitting
        # and set the user who posted it to the current logged in user
        form.instance.posted_by = self.request.user
        # now validate the form
        return super().form_valid(form)


class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, pk=kwargs['object'].id)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context["has_user_saved_book"] = profile.favourites.filter(
                id=book.id).exists()
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'language', 'genre', 'description', 'image']
    success_message = 'Book "%(title)s" was updated successfully!'

    def test_func(self):
        return is_user_admin_or_book_owner(self)


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book

    def get_success_url(self):
        messages.success(self.request, 'Book was deleted successfully!')
        # https://stackoverflow.com/questions/48669514/difference-between-reverse-and-reverse-lazy-in-django
        return reverse("my_books")

    def test_func(self):
        return is_user_admin_or_book_owner(self)

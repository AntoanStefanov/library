from django.shortcuts import render
from django.views.generic import ListView

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = 'books/home.html'
    ordering = ['-date_posted']
    # change object_list variable
    context_object_name = 'books'
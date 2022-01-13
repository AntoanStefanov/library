from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView

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


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'image']

    def form_valid(self, form):
        # take the form instance before submitting 
        # and set the user who posted it to the current logged in user
        form.instance.posted_by = self.request.user
        # now validate the form
        return super().form_valid(form)

    # template -> book_form.html (<app name>_form.html)

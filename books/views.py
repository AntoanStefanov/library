from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import FormMixin
from library_project.utils import is_user_admin_or_book_owner

from books.forms import BookForm, BookOrderForm, CommentForm

from .models import Book


class BookListView(FormMixin, ListView):
    """
        https://stackoverflow.com/questions/32513756/validate-django-form-get-request
    """
    model = Book
    form_class = BookOrderForm
    template_name = 'books/book_list.html'
    # change object_list variable for template use
    context_object_name = 'books'
    # pagination
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(self.request.GET)
        self.order_by = None
        if form.is_valid():
            self.order_by = form.cleaned_data['order_by']
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
            By default, the order is date_posted(newest), 
            check CommonFields model Meta class in books/models.py.
            If view has order_by property (in get method *checks if passed form is valid),
            order query. Else return query by default.
        """
        query = Book.objects.all()
        if self.order_by:
            query = query.order_by(self.order_by)
        return query


class FavouritesView(LoginRequiredMixin, BookListView):
    def get_queryset(self):
        profile = self.request.user.profile
        # profile.favourites -> ManyRelatedManager
        favourites = profile.favourites.all()

        if self.order_by:
            favourites = favourites.order_by(self.order_by)
        return favourites


class RecommendedBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/recommended_book_list.html'
    # change object_list variable for template use
    context_object_name = 'books'

    def get_queryset(self):
        """
            # Book.likes.through.objects - returns Manager for 'users_profile_likes' table in DB
            # Book.likes.through.objects.all() - returns all likes in this table.

            # https://stackoverflow.com/questions/21662974/django-order-by-most-frequent-value
            # Book.likes.through.objects -> returns Manager(which has 'all' method also) for 'users_profile_likes' table in DB

            1.1 Book.likes.through.objects.values_list('book_id') ->
            # QuerySet [(17,), (17,), (23,), (17,), (23,), (16,), (17,), (23,), (16,), (15,)]>

            1.1 OR 1.2 (https://docs.djangoproject.com/en/4.0/ref/models/querysets/#values-list)

            1.2 Book.likes.through.objects.values_list('book_id', flat=True) -> 
            # <QuerySet [17, 17, 23, 17, 23, 16, 16, 15, 23, 17]>

            # .annotate(likes_count=Count('book_id')) ->
            2.1 <QuerySet [(23, 3), (17, 4), (15, 1), (16, 2)]>
            # OR #
            2.2 <QuerySet [23, 17, 15, 16]>

            # .order_by('-likes_count',  'book_id__title') ->
            'book_id__title' -> if likes are equal then sort by title.

            3.1 <QuerySet [(17, 4), (23, 3), (16, 2), (15, 1)]>
            # OR #
            3.2 <QuerySet [17, 23, 16, 15]>
            # [:3] ->
            4.1 <QuerySet [(17, 4), (23, 3), (16, 2)]>
            # OR #
            4.2 <QuerySet [17, 23, 16]>
        """

        # CHECK DOCS in this function!
        first_three_most_liked_book_ids = Book.likes.through.objects.values_list(
            'book_id', flat=True).annotate(likes_count=Count('book_id')).order_by('-likes_count', 'book_id__title')[:3]

        # https://stackoverflow.com/questions/9304908/how-can-i-filter-a-django-query-with-a-list-of-values
        three_most_liked_books = Book.objects.filter(
            pk__in=list(first_three_most_liked_book_ids))

        # https://stackoverflow.com/questions/4916851/django-get-a-queryset-from-array-of-ids-in-specific-order
        # DB QUERIES OBJECTS AND SAVE IT WHEN FIRST IS READY ! NO ORDER IN DB QUERY
        three_most_liked_books = dict(
            [(obj.id, obj) for obj in three_most_liked_books])
        three_most_liked_books_sorted = [
            three_most_liked_books[id] for id in first_three_most_liked_book_ids]

        return three_most_liked_books_sorted


class GenreBookListView(LoginRequiredMixin, BookListView):

    def get(self, request, *args, **kwargs):
        """
            Check if genre passed in url is a valid argument.
            If not redirect to library.
        """
        genre = kwargs.get('genre')
        if genre not in [choices[0] for choices in Book.GENRE_CHOICES]:
            return redirect(reverse('books_library'))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        genre = self.kwargs.get('genre')
        genre_books = Book.objects.filter(
            genre=genre)

        if self.order_by:
            genre_books = genre_books.order_by(self.order_by)
        return genre_books


class AuthorBookListView(BookListView):
    def get_queryset(self):
        author = self.kwargs.get('author')
        author_books = Book.objects.filter(
            author=author)

        if self.order_by:
            author_books = author_books.order_by(self.order_by)
        return author_books


class ProfileBookListView(LoginRequiredMixin, BookListView):
    def get_queryset(self):
        profile_username = self.kwargs.get('profile')
        profile_books = Book.objects.filter(
            posted_by__username=profile_username)

        if self.order_by:
            profile_books = profile_books.order_by(self.order_by)
        return profile_books


class MyBookListView(LoginRequiredMixin, BookListView):

    def get_queryset(self):
        # foreignkey -> reverse_many_to_one_manager method(all()),
        user_books = self.request.user.book_set.all()
        # user_books = Book.objects.filter(
        # posted_by=self.request.user.pk)

        if self.order_by:
            user_books = user_books.order_by(self.order_by)
        return user_books


class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # LoginRequiredMixin -> IF NOT LOGGED USER TRIES TO CREATE A BOOK - redirect to LOGIN_URL !
    # LOGIN_URL = 'login' (path func - name)
    model = Book
    form_class = BookForm
    success_message = 'Book "%(title)s" was created successfully!'

    def form_valid(self, form):
        # take the form instance before submitting
        # and set the user who posted it to the current logged in user
        form.instance.posted_by = self.request.user
        # now validate the form
        return super().form_valid(form)


class BookDetailsView(FormMixin, DetailView):
    """
        https://stackoverflow.com/questions/45659986/django-implementing-a-form-within-a-generic-detailview
    """
    model = Book
    template_name = 'books/book_details.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context["has_user_saved_book"] = profile.favourites.filter(
                id=book.id).exists()

            context["has_user_liked_book"] = profile.likes.filter(
                id=book.id).exists()

            context["comments"] = book.comment_set.all()

            # self.form_invalid(form) *in post method* returns
            # self.render_to_response(self.get_context_data(form=form))
            # so if a form was invalid , the form_invalid method
            # will pass a form with the errors in the context
            # this check if form is passed from that method, and if IT IS passed, do not create a new form instance.
            # so that the error messages will be displayed.
            if 'form' not in context:
                context['form'] = CommentForm()

        context["number_of_likes"] = book.likes.count()

        return context

    def post(self, request, *args, **kwargs):
        # in form valid 'self.object' is needed.
        self.object = self.get_object()
        # put data in form.
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Commented succesfully!')
            return self.form_valid(form)
        else:
            messages.error(request, 'Commented unsuccesfully!')
            return self.form_invalid(form)

    def form_valid(self, form):
        """
            If form is valid. Pass who commented, the book to the form and save it.
            Get back to the current book details page.
        """
        form.instance.posted_by = self.request.user
        form.instance.book = self.object
        form.save()
        # get url in string format, then pass it to redirect for HTTP response.
        return redirect(self.object.get_absolute_url())


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
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

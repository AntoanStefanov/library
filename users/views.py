from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from library_project.utils import is_user_admin_or_profile_owner
from books.models import Book

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


# https://stackoverflow.com/questions/10018757/how-does-the-order-of-mixins-affect-the-derived-class
# https://docs.djangoproject.com/en/4.0/ref/contrib/messages/#adding-messages-in-class-based-views
class UserRegisterView(SuccessMessageMixin, CreateView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class
    # The form class to instantiate.
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    # The cleaned data from the form is available for string interpolation using the %(field_name)s syntax
    success_message = 'Your profile was created successfully, %(username)s!'

    # https://stackoverflow.com/questions/2320581/django-redirect-logged-in-users-from-login-page
    # Think of dispatch method as a middleman between requests and responses
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('website_home')
        return super().dispatch(*args, **kwargs)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Account has been deleted successfully!')
        return reverse("website_home")

    def test_func(self):
        return is_user_admin_or_profile_owner(self)


class UserFavouritesView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'books'
    template_name = 'users/favourites.html'
    paginate_by = 2

    def get_queryset(self):
        profile = self.request.user.profile
        # profile.favourites -> ManyRelatedManager
        favourites = profile.favourites.all()
        return favourites


@login_required
def user_profile_view(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)

        profile_update_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(
                request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
        'user': request.user
    }

    return render(request, 'users/profile.html', context)


@login_required
def user_add_favourite_view(request, **kwargs):
    # https://docs.djangoproject.com/en/4.0/topics/http/shortcuts/#get-object-or-404
    # https://www.youtube.com/watch?v=H4QPHLmsZMU
    book = get_object_or_404(Book, pk=kwargs.get('pk'))
    profile = request.user.profile
    if profile.favourites.filter(id=book.id).exists():
        profile.favourites.remove(book)
    else:
        profile.favourites.add(book)

    return redirect(reverse('books_details', kwargs={'pk': book.id, 'slug': book.slug}))

@login_required
def user_like_book_view(request, **kwargs):
    book = get_object_or_404(Book, pk=kwargs.get('pk'))
    profile = request.user.profile
    if profile.likes.filter(id=book.id).exists():
        profile.likes.remove(book)
    else:
        profile.likes.add(book)

    return redirect(reverse('books_details', kwargs={'pk': book.id, 'slug': book.slug}))
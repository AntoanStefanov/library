from books.models import Book
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from library_project.utils import delete_profile_or_book_image, is_user_admin_or_profile_owner

from users.models import Profile, ProfileFavouriteBooks

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
    context_object_name = 'user_profile'

    def get_success_url(self):
        messages.success(
            self.request, 'Account has been deleted successfully!')
        return reverse("website_home")

    def test_func(self):
        """
            UserPassesTestMixin (check mixin), needs to be overrided.
        """
        return is_user_admin_or_profile_owner(self)

    # def get_context_object_name(self, obj):
    #     # OVERRIDE, SO THAT this method doesn't override user variable in templates!
    #     pass

class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_details.html'


@login_required
def user_profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=user)

        profile_update_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            delete_profile_or_book_image(
                instance=user.profile, form=profile_update_form)
            user_update_form.save()
            profile_update_form.save()
            messages.success(
                request, f'Your account has been updated!')
            return redirect('profile')
    else:
        # Current user should be profile owner or admin, superuser

        if user.is_superuser and user != request.user:
            # If admin tries to edit superuser profile, redirect.
            # Only superuser can edit his own profile.
            return redirect('books_library')

        if request.user.is_superuser or request.user.id == pk or request.user.groups.filter(name='full-CRUD').exists():
            user_update_form = UserUpdateForm(instance=user)
            profile_update_form = ProfileUpdateForm(instance=user.profile)
        else:
            return redirect('books_library')

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
        'user_profile': user
    }

    return render(request, 'users/profile.html', context)


@login_required
def user_save_book_view(request, **kwargs):
    # https://docs.djangoproject.com/en/4.0/topics/http/shortcuts/#get-object-or-404
    # https://www.youtube.com/watch?v=H4QPHLmsZMU
    book = get_object_or_404(Book, pk=kwargs.get('pk'))
    profile = request.user.profile
    saved_book = ProfileFavouriteBooks.objects.filter(
        user_id=profile.user_id,
        book_id=book.id
    )

    if saved_book.exists():
        saved_book.delete()
    else:
        ProfileFavouriteBooks.objects.create(
            user_id=profile.user_id,
            book_id=book.id
        )

    return redirect(book.get_absolute_url())


@login_required
def user_like_book_view(request, **kwargs):
    book = get_object_or_404(Book, pk=kwargs.get('pk'))
    profile = request.user.profile
    if profile.likes.filter(id=book.id).exists():
        profile.likes.remove(book)
    else:
        profile.likes.add(book)

    return redirect(book.get_absolute_url())

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

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


@login_required
def profile(request):
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
        'profile_update_form': profile_update_form
    }

    return render(request, 'users/profile.html', context)

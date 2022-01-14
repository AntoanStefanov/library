from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from .forms import UserRegisterForm


# https://stackoverflow.com/questions/10018757/how-does-the-order-of-mixins-affect-the-derived-class
# https://docs.djangoproject.com/en/4.0/ref/contrib/messages/#adding-messages-in-class-based-views
class UserRegisterView(SuccessMessageMixin, CreateView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class
    # The form class to instantiate.
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = '/login/'
    # The cleaned data from the form is available for string interpolation using the %(field_name)s syntax
    success_message = 'Your profile was created successfully, %(username)s!'

    # https://stackoverflow.com/questions/2320581/django-redirect-logged-in-users-from-login-page
    # Think of dispatch method as a middleman between requests and responses
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('books_home')
        return super().dispatch(*args, **kwargs)
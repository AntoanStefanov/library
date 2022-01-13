from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
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

    # Logged users not allowed to register page.
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        form = self.form_class() 
        return render(request, self.template_name, {'form': form})
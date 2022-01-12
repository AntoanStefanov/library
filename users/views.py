from django.views.generic.edit import CreateView

from .forms import UserRegisterForm


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    success_url = '/login/'
    form_class = UserRegisterForm

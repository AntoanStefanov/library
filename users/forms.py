from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(UserCreationForm):
    # email here because in AbstractUser, email is not required
    email = forms.EmailField(
        help_text="Email must be unique. Include '@' in email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_field
    def clean_email(self):
        # https://youtu.be/wVnQkKf-gHo?t=287
        email = self.cleaned_data.get('email')

        # flat=True, to return a list, not a list with tuples.
        if email in User.objects.values_list('email', flat=True):
            raise forms.ValidationError('Email already exists.')
        return email

    # Example code, if needed.
    # def clean(self):
    #     """
    #         Puts validations error above all fields.
    #     """
    #     cleaned_data = super().clean()
    #     first_name = cleaned_data.get('username')
    #     last_name  = cleaned_data.get('password1')

    #     if first_name == last_name:
    #         raise forms.ValidationError( "username and password1 cannot be the same." )


class UserUpdateForm(forms.ModelForm):
    # email here because in AbstractUser, email is not required

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

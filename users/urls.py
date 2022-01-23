from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import (UserDeleteView, UserFavouritesView, UserRegisterView,
                    profile, add_favourite)

urlpatterns = [
    # DOCS LoginView ->
    # https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.views.LoginView.get_default_redirect_url
    # LOGIN_REDIRECT_URL = 'website_home'
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),  name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', include([
        path('', profile, name='profile'),
        path('delete/<int:pk>/', UserDeleteView.as_view(), name='profile_delete'),
        path('add_favourite/<int:pk>/', add_favourite, name='profile_add_favourite'),
        path('favourites/', UserFavouritesView.as_view(), name='profile_favourites'),
    ]))
]

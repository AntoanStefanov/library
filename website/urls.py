from django.urls import include, path

from .views import AboutView, HomeView, admin_view

# https://stackoverflow.com/questions/40914554/django-views-in-project-directory/58366377

urlpatterns = [
    path('', HomeView.as_view(), name='website_home'),
    path('about/', AboutView.as_view(), name='website_about'),
    path('books/', include('books.urls')),
    path('users/', include('users.urls')),
    path('admin_part/', admin_view, name='website_admin_part'),

]

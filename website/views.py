from books.models import Book
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'website/home.html'


class AboutView(TemplateView):
    template_name = 'website/about.html'


def admin_view(request):
    if request.user.is_superuser or request.user.groups.filter(name__in=['full-CRUD', 'limited-CRUD']).exists():
        context = {
            'books': Book.objects.all().order_by('title', 'author'),
            'users': User.objects.all().order_by('username', 'email'),
        }
        return render(request, 'website/admin_part.html', context)
    return redirect('website_home')

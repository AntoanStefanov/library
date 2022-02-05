from django import template
from books.models import Book

register = template.Library()

@register.inclusion_tag('website/tags/genre_list.html')
def all_genres():
    """
        https://youtu.be/ZYoJjdUHNZA?t=8274
    """
    return {'genres':  Book.GENRE_CHOICES}
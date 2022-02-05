from django import template
from books.models import Book

register = template.Library()

@register.inclusion_tag('website/tags/genre_list.html')
def all_genres():
    return {'genres': [choice[1] for choice in Book.GENRE_CHOICES]}
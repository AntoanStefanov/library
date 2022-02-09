from django import forms

from books.models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ('date_posted', 'slug', 'posted_by')

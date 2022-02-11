from django import forms

from books.models import Book, Comment


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ('date_posted', 'slug', 'posted_by')


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content',)

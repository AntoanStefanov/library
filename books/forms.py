from django import forms

from books.models import Book, Comment


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Book
        exclude = ('date_posted', 'slug', 'posted_by')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

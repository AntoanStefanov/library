from django import forms

from books.models import Book, Comment


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].label += ":"

    class Meta:
        model = Book
        exclude = ('date_posted', 'slug', 'posted_by')

    # Create form validation if a book with same name OR SLUG already exists.

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

    # Create form validation if a comment contains bad words ?.

class BookOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_by'].label = "Sort By"

    order_by = forms.ChoiceField(
        choices=(
            ('-date_posted', 'Date added(newest)'),
            ('date_posted', 'Date added(oldest)'),
            ('title', 'Title'),
            ('author', 'Author'),
            ('language', 'Language'),
        )
    )

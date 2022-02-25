from django import forms
from django.utils.text import slugify

from books.models import Book, Comment


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].label += ":"

    class Meta:
        model = Book
        exclude = ('date_posted', 'slug', 'posted_by')

    def clean(self):
        # https://georgexyz.com/django-model-form-validation.html - clean for multiple fields
        title = self.cleaned_data.get('title')
        author = self.cleaned_data.get('author')
        possible_slug = slugify(f"{title} {author}")
        if possible_slug in Book.objects.values_list('slug', flat=True):
            raise forms.ValidationError(
                'Book with given title and author already exists!')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

    # Create form validation if a comment contains bad words ?


class BookOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_by'].label = "Sort By"

    CHOICES = (
        ('-date_posted', 'Date added(newest)'),
        ('date_posted', 'Date added(oldest)'),
        ('title', 'Title'),
        ('author', 'Author'),
        ('language', 'Language'),
    )

    order_by = forms.ChoiceField(
        choices=CHOICES
    )

    def clean_order_by(self):
        # https://youtu.be/wVnQkKf-gHo?t=287
        order_by = self.cleaned_data.get('order_by')

        params = [choice[0] for choice in self.CHOICES]

        if order_by not in params:
            raise forms.ValidationError('Invalid Order Paramater.')
        return order_by

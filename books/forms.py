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
        # https://docs.djangoproject.com/en/4.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
        # https://stackoverflow.com/questions/39488816/django-form-clean-run-before-field-validators
        # https://georgexyz.com/django-model-form-validation.html - clean for multiple fields
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        possible_slug = slugify(f"{title} {author}")
        if possible_slug in Book.objects.values_list('slug', flat=True):
            raise forms.ValidationError(
                'Book with given title and author already exists!')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

    BAD_WORDS = ['idiot', 'fool', 'stupid']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        words = content.split(' ')

        for word in words:
            if word.lower() in self.BAD_WORDS:
                raise forms.ValidationError(
                    'Offensive words are not allowed !')
        return content


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

    # order_by is checked in BookListView - get method.
    def clean_order_by(self):
        # https://youtu.be/wVnQkKf-gHo?t=287
        order_by = self.cleaned_data.get('order_by')

        params = [choice[0] for choice in self.CHOICES]

        if order_by not in params:
            raise forms.ValidationError('Invalid Order Paramater.')
        return order_by

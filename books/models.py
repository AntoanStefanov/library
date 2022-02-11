from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from library_project.utils import is_image_resizable


class CommonFields(models.Model):
    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#foreignkey
    # one-to-many relationship -> cascade -> del all books if user is deleted.
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    # default=timezonenow - able to override
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        """
            Give model additional meta information/options.
            Anything that's not a field.
            https://docs.djangoproject.com/en/4.0/topics/db/models/#meta-options
        """

        abstract = True
        ordering = ['-date_posted']


class Book(CommonFields):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 150

    AUTHOR_MAX_LENGTH = 100
    AUTHOR_MIN_LENGTH = 2

    LANGUAGE_MAX_LENGTH = 50
    LANGUAGE_MIN_LENGTH = 2

    # answer the question why to use variables.
    # https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django
    GENRE_ART = 'ART'
    GENRE_BIOGRAPHY = 'BIOGRAPHY'
    GENRE_COMEDY = 'COMEDY'
    GENRE_CLASSIC = 'CLASSIC'
    GENRE_HEALTH = 'HEALTH'
    GENRE_HISTORY = 'HISTORY'
    GENRE_THRILLER = 'THRILLER'
    GENRE_OTHER = 'OTHER'

    GENRE_CHOICES = [
        (GENRE_ART, 'Art'),
        (GENRE_BIOGRAPHY, 'Biography'),
        (GENRE_COMEDY, 'Comedy'),
        (GENRE_CLASSIC, 'Classic'),
        (GENRE_HEALTH, 'Health'),
        (GENRE_HISTORY, 'History'),
        (GENRE_THRILLER, 'Thriller'),
        (GENRE_OTHER, 'Other'),
    ]

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=[MinLengthValidator(TITLE_MIN_LENGTH)]
    )

    author = models.CharField(
        max_length=AUTHOR_MAX_LENGTH,
        validators=[MinLengthValidator(AUTHOR_MIN_LENGTH)]
    )

    language = models.CharField(
        max_length=LANGUAGE_MAX_LENGTH,
        validators=[MinLengthValidator(LANGUAGE_MIN_LENGTH)]
    )

    genre = models.CharField(
        max_length=max(len(choices[0]) for choices in GENRE_CHOICES),
        choices=GENRE_CHOICES,
        default=GENRE_ART
    )

    description = models.TextField()

    image = models.ImageField(
        default='default_book.jpg',
        upload_to='books_pics',
    )

    # https://learndjango.com/tutorials/django-slug-tutorial
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
            Overriding save method to resize uploaded image if needed,
            no need an image to be more than 400x500 px.

            Using title and author , making slug being less likely to match with another slug.
            slugify docs -> https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.text.slugify

            https://stackoverflow.com/questions/65267519/how-to-update-str-and-slug-everytime-after-djangos-model-update
        """

        self.slug = slugify(f"{self.title} {self.author}")
        super().save(*args, **kwargs)
        is_image_resizable(self.image.path)

    def get_absolute_url(self):
        """
            Method that gets called whenever a book is created or updated.
            https://docs.djangoproject.com/en/4.0/ref/models/instances/#get-absolute-url
            https://docs.djangoproject.com/en/4.0/ref/urlresolvers/#django.urls.reverse
        """
        # The most basic difference between the two is :
        # - Redirect Method will redirect you to a specific route in General.
        # - Reverse Method will return the complete URL to that route as a String.
        return reverse('books_details', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(CommonFields):
    CONTENT_MIN_LENGTH = 5

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(
        validators=[MinLengthValidator(CONTENT_MIN_LENGTH)])

    def __str__(self):
        return self.content

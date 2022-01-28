from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from library_project.utils import is_image_resizable


class Book(models.Model):

    class Meta:
        """
            Give Book model additional meta information/options.
            Anything that's not a field.
            https://docs.djangoproject.com/en/4.0/topics/db/models/#meta-options
        """

        ordering = ['-date_posted']

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

    # Large max_length in case unicode chars are used.
    # One unicode character is many characters.
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    genre = models.CharField(
        max_length=10, choices=GENRE_CHOICES, default=GENRE_ART)
    description = models.TextField()
    image = models.ImageField(
        default='default_book.jpg', upload_to='books_pics')
    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    # default=timezonenow - able to override
    date_posted = models.DateTimeField(default=timezone.now)

    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#foreignkey
    # one-to-many relationship -> cascade -> del all books if user is deleted.
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # https://learndjango.com/tutorials/django-slug-tutorial
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
            Overriding save method to resize uploaded image if needed,
            no need an image to be more than 400x500 px.
        """
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

    def save(self, *args, **kwargs):
        """
            Overriding save method, so that a slug is created automatically.
            Using title and author , making slug being less likely to match with another slug.
            slugify docs -> https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.text.slugify
        """
        if not self.slug:
            self.slug = slugify(
                f"{self.title} {self.author}")
        return super().save(*args, **kwargs)

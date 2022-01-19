from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from library_project.utils import is_image_resizable


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    language = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(
        default='default_book.jpg', upload_to='books_pics')
    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    # default=timezonenow - able to override
    date_posted = models.DateTimeField(default=timezone.now)

    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#foreignkey
    # many-to-one relationship -> cascade -> del all books if user is deleted.
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # https://learndjango.com/tutorials/django-slug-tutorial
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
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
        return reverse('book_details', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        """
            Overriding save method, so that a slug is created automatically.
            Using title and author , making slug being less likely to match with another slug.
            slugify docs -> https://docs.djangoproject.com/en/4.0/ref/utils/#django.utils.text.slugify
            Info for allow_unicode and allowing URLs to work with unicode:
            https://stackoverflow.com/questions/50321644/django-not-matching-unicode-in-url
            https://docs.djangoproject.com/en/4.0/topics/http/urls/#path-converters
        """
        if not self.slug:
            self.slug = slugify(
                f"{self.title} {self.author}", allow_unicode=True)
        return super().save(*args, **kwargs)

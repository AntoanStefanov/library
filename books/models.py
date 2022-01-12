from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='books_pics')
    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    # default=timezonenow - able to override
    date_posted = models.DateTimeField(default=timezone.now)

    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#foreignkey
    # many-to-one relationship -> cascade -> del all books if user is deleted.
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # https://docs.djangoproject.com/en/4.0/ref/models/instances/#get-absolute-url
        # https://docs.djangoproject.com/en/4.0/ref/urlresolvers/#django.urls.reverse
        return reverse('books_library')

from books.models import Book
from django.contrib.auth.models import User
from django.db import models
from library_project.utils import is_image_resizable


class Profile(models.Model):
    # cascade -> if user is deleted, delete the profile too
    # but if we delete the profile, it won't delete the user
    # JUST ONE WAY thing , MAKE IT TWO WAY THING

    image = models.ImageField(
        default='default_user.jpg',
        upload_to='profile_pics'
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True)

    # Could be done with another Model "FavouriteBook" if needed.
    favourites = models.ManyToManyField(Book, blank=True)

    # Could be done with another Model "Like" if needed.
    # https://stackoverflow.com/questions/2606194/django-error-message-add-a-related-name-argument-to-the-definition - related_name
    likes = models.ManyToManyField(Book, blank=True, related_name="likes")

    # when I make a change in a model , also it will make a change in the DB
    # to apply changes -> make migrations(prepare SQL code) -> migrate(update the DB)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        is_image_resizable(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'

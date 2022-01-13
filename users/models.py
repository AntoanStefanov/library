from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    # cascade -> if user is deleted, delete the profile too
    # but if we delete the profile, it won't delete the user
    # JUST ONE WAY thing , MAKE IT TWO WAY THING
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # when I make a change in a model , also it will make a change in the DB
    # to apply changes -> make migrations(prepare SQL code) -> migrate(update the DB)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # that will resize the image
            img.thumbnail(output_size)
            img.save(self.image.path)

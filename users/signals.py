# Create a user-profile for each user that has registered

from django.db.models.signals import post_save, post_delete
# post_save -> signal that gets fired AFTER an object is saved
# we need post_save signal when a user is registered
from django.contrib.auth.models import User
# User here is the sender, User sends the signal
from django.dispatch import receiver
# a reciever is a function that gets this signal and the perfoms some task
from .models import Profile
# we need Profile since we are creating a profile in our function


# reciever is the create_profile func
# takes all args that post_save signal passed to it
# runs everytime when a user gets created.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # if a user was created, then create a profile with that User instance
    # in case user is not specified
    if created:
        Profile.objects.create(user=instance)

# Do we need save_profile func doesn't create calls save() internally ?
# save the profile instance when the user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# https://stackoverflow.com/questions/12754024/onetoonefield-and-deleting
# del user if profile has been deleted
@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    # in case user is not specified
    if instance.user:
        instance.user.delete()
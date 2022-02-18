import os
from PIL import Image


def is_image_resizable(path):
    """ Check if image has large resolution, if so, resize it. """

    img = Image.open(path)

    if img.width > 400 or img.height > 500:
        output_size = (400, 500)
        # that will resize the image
        img.thumbnail(output_size)
        img.save(path)


def is_user_admin_or_book_owner(view):
    """ Check if user is admin or owner of current book. """

    book = view.get_object()
    current_user = view.request.user

    return current_user == book.posted_by or current_user.is_superuser


def is_user_admin_or_profile_owner(view):
    """ Check if user is admin or owner of profile. """

    user = view.get_object()
    current_user = view.request.user

    return current_user == user or current_user.is_superuser


def delete_profile_or_book_image(object):
    image = object.image

    if image.name != 'default_user.jpg' and image.name != 'default_book.jpg':
        image_path = image.path
        os.remove(image_path)

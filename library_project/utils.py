import os
from PIL import Image


def is_image_resizable(path):
    """ Check if image has large resolution, if so, resize it. """

    img = Image.open(path)
    output_size = (368, 500)
    # save width-height ratio.
    img = img.resize(output_size)
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


def delete_profile_or_book_image(instance=None, form=None):
    """
        When updating , instance doesn't have the previous image,
        so that's why we use form if needed.
    """
    if form:
        image = form.initial.get('image')
        current_image = instance.image
        # check if image hasn't been changed, if not do not delete.
        if image == current_image:
            return
    else:
        image = instance.image

    if image.name != 'default_user.jpg' and image.name != 'default_book.jpg':
        image_path = image.path
        os.remove(image_path)


def megabytes_to_bytes(value):
    return value * 1024 * 1024

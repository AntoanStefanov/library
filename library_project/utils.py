import os
from PIL import Image


def is_image_resizable(path):
    """ Check if image has large resolution, if so, resize it. """

    with Image.open(path) as img:
        if img.width != 368 and img.height != 500:
            output_size = (368, 500)
            # save width-height ratio.
            img = img.resize(output_size)
            img.save(path)


def is_user_admin_or_book_owner(view):
    """ Check if user is admin or owner of current book. """

    book = view.get_object()
    current_user = view.request.user

    return current_user == book.posted_by or current_user.is_superuser or current_user.groups.filter(name='full-CRUD').exists()


def is_user_admin_or_profile_owner(view):
    """ Check if user is admin or owner of profile. """

    user = view.get_object()
    current_user = view.request.user

    if user.is_superuser and user != current_user:
        # ONLY superuser can delete and modify his acc
        return False

    return current_user == user or current_user.is_superuser or current_user.groups.filter(name='full-CRUD').exists()


def is_user_admin_or_comment_owner(view):

    user = view.get_object()
    current_user = view.request.user

    return current_user == user or current_user.is_superuser or current_user.groups.filter(name__in=['limited-CRUD', 'full-CRUD']).exists()


def delete_profile_or_book_image(instance=None, form=None):
    """
        When updating , instance doesn't have the previous image,
        so that's why we use form if needed.
        Check if image is default, so that we dont delete it,
        Error Handling with if's instead of try/except blocks.
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

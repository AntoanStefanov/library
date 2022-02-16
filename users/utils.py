import os


def delete_profile_image(profile):
    profile_image = profile.image

    if profile_image.name != 'default_user.jpg':
        image_path = profile_image.path
        os.remove(image_path)

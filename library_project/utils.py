from PIL import Image


def is_image_resizable(path):

    img = Image.open(path)
    
    if img.width > 200 or img.height > 300:
        output_size = (200, 300)
        # that will resize the image
        img.thumbnail(output_size)
        img.save(path)

def is_user_admin_or_book_owner(view):
    book = view.get_object()
    current_user = view.request.user
        
    return current_user == book.posted_by or current_user.is_superuser
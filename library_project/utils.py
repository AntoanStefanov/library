from PIL import Image

def is_image_resizable(path):

    img = Image.open(path)
    
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        # that will resize the image
        img.thumbnail(output_size)
        img.save(path)
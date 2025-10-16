import os
from django.utils.text import slugify

def avatar_path(instance, filename):
    extension = filename.split('.')[-1]

    clean_filename = slugify(os.path.splitext(filename)[0])
    return f'avatares/{instance.username}/{clean_filename}.{extension}'
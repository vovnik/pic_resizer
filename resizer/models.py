from django.db import models
from django.core.files import File

import requests
from PIL import Image
from urllib.parse import urlsplit, quote
from os.path import basename
from tempfile import TemporaryFile
from os.path import join


class Picture(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now=True)
    last_resized_at = models.DateTimeField(null=True)
    original_picture = models.ImageField(upload_to='original', null=True)
    resized_picture = models.ImageField(upload_to='resized', null=True)

    def download_picture_from_url(self, url):
        with TemporaryFile() as tf:
            request = requests.get(url, stream=True)
            for chunk in request.iter_content(chunk_size=4096):
                tf.write(chunk)

            tf.seek(0)
            self.original_picture.save(self.name, File(tf))

    def resize_picture(self, size):
        if self.resized_picture:
            self.resized_picture.delete()  # мы не храним несколько вариантов картинок

        original_img = Image.open(self.original_picture)
        resized_img = original_img.resize(size, resample=3)
        # получаем расширение картинки
        extension = self.name.split('.')[-1].upper()
        if extension == 'JPG' or extension is None:
            extension = 'JPEG'
        with TemporaryFile() as tf:
            resized_img.save(tf, format=extension)
            self.resized_picture.save(self.name, File(tf))

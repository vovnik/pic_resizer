from django.test import TestCase
from django.db.models.fields.files import ImageFieldFile
from resizer.models import Picture
from os.path import join

class PictureTest(TestCase):

    def setUp(self):
        self.pic_img = Picture.objects.create(
            name='homer.jpg', original_picture=join('test', 'homer.jpg'))
        self.pic_png = Picture.objects.create(
            name='castaway.png', original_picture=join('test', 'castaway.png'))
        self.pic_webp = Picture.objects.create(
            name='cat.webp', original_picture=join('test', 'cat.webp'))

        self.size = (480, 360)
        self.url = 'https://hhcdn.ru/employer-logo/3385106.png'

        self.filename = '3385106.png'
        self.picture_from_url = Picture(id=1, name=self.filename)

    def test_original_picture(self):
        picture = Picture.objects.get(id=self.pic_img.id)
        original_picture = picture.original_picture
        self.assertEquals(original_picture, join('test', 'homer.jpg'))
        picture = Picture.objects.get(id=self.pic_png.id)
        original_picture = picture.original_picture
        self.assertEquals(original_picture, join('test', 'castaway.png'))

        picture = Picture.objects.get(id=self.pic_webp.id)
        original_picture = picture.original_picture
        self.assertEquals(original_picture, join('test', 'cat.webp'))

    def test_resize_picture(self):
        Picture.resize_picture(self.pic_img, self.size)
        Picture.resize_picture(self.pic_png, self.size)
        Picture.resize_picture(self.pic_webp, self.size)

        self.assertIsInstance(self.pic_img.resized_picture, ImageFieldFile)
        self.assertIsInstance(self.pic_png.resized_picture, ImageFieldFile)
        self.assertIsInstance(self.pic_webp.resized_picture, ImageFieldFile)

    def test_download_picture_from_url(self):
        self.picture_from_url.download_picture_from_url(self.url)
        self.picture_from_url.save()
        self.assertIsInstance(
            self.picture_from_url.resized_picture, ImageFieldFile)

    def tearDown(self):
        pass

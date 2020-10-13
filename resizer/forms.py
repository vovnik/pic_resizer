from django import forms
from resizer.models import Picture

import requests
import requests.exceptions as rex
from os.path import basename
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlsplit


class PictureForm(forms.Form):
    picture = forms.ImageField(required=False)
    picture_url = forms.CharField(required=False)

    def clean_picture_url(self):
        url = self.cleaned_data['picture_url']
        if not url:
            return None
        try:
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            # если по ссылке не окажется картинки, то будет обработано исключение
            picture = Image.open(response.raw)
            return url
        except (rex.MissingSchema, rex.InvalidSchema):
            self.add_error(
                'picture_url', 'Введённая строка не является корректной ссылкой.')
            return None
        except (rex.ConnectionError, rex.HTTPError):
            self.add_error(
                'picture_url', 'Не удалось загрузить изображение по ссылке.')
            return None
        except UnidentifiedImageError:
            self.add_error(
                'picture_url', 'По указанной ссылке нельзя получить изображение.')

    def clean(self):
        # Исключающее ИЛИ для загрузки только из одного источника
        if bool(self.cleaned_data.get('picture')) ^ bool(self.cleaned_data.get('picture_url')):
            return self.cleaned_data
        raise forms.ValidationError(
            u'Должно быть заполнено одно поле для источника изображения!')

    def save(self):
        if self.cleaned_data.get('picture'):
            picture = self.cleaned_data['picture']
            picture = Picture(original_picture=picture,
                              name=picture.name)
            picture.save()
            return picture
        url = self.cleaned_data.get('picture_url')
        name = basename(urlsplit(url).path)
        picture = Picture(name=name)
        picture.download_picture_from_url(url)
        picture.save()
        return picture


class ResizeForm(forms.Form):
    width = forms.IntegerField(required=False, label='Ширина')
    height = forms.IntegerField(required=False, label='Высота')

    def clean_width(self):
        if self.cleaned_data['width'] < 1:
            self.add_error(
                'width', 'Количество пикселей должно быть больше нуля!')
            return None
        return self.cleaned_data['width']

    def clean_height(self):
        if self.cleaned_data['height'] < 1:
            self.add_error(
                'height', 'Количество пикселей должно быть больше нуля!')
            return None
        return self.cleaned_data['height']

    def clean(self):
        if self.cleaned_data.get('width') is None and self.cleaned_data.get('height') is None:
            raise forms.ValidationError(
                u'Введите хотя бы в одно поле целое число пикселей')

        if self.cleaned_data.get('width') is not None and self.cleaned_data.get('height') is None:
            self.cleaned_data['height'] = self.cleaned_data['width']

        elif self.cleaned_data.get('height') is not None and self.cleaned_data.get('width') is None:
            self.cleaned_data['width'] = self.cleaned_data['height']

        return self.cleaned_data

    def save(self, picture_id):
        size = (self.cleaned_data['width'], self.cleaned_data['height'])
        picture = Picture.objects.get(id=picture_id)
        picture.resize_picture(size)

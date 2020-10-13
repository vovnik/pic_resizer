from django.shortcuts import render, redirect
from django.conf import settings
from resizer.forms import PictureForm, ResizeForm
from resizer.models import Picture


def index(request):
    return render(request, 'index.html', {"pictures": Picture.objects.all()})


def picture_upload(request):
    if request.method == 'POST':
        if request.FILES:
            form = PictureForm(request.POST, request.FILES)
        else:
            form = PictureForm(request.POST)
        if form.is_valid():
            picture = form.save()
            return redirect(f'/picture/{picture.id}')
    else:
        form = PictureForm()
    return render(request, 'upload.html', {
        'form': form
    })


def picture_resize(request, picture_id):
    picture = Picture.objects.get(id=picture_id)
    if request.method == 'POST':
        form = ResizeForm(request.POST)
        if form.is_valid():
            form.save(picture_id)
            picture = Picture.objects.get(id=picture_id)
            img_url = 'pictures/' + picture.resized_picture.name
            return render(request, 'picture.html', {
                'form': form,
                'img_url': img_url
            })
    else:
        form = ResizeForm(initial={
            'width': picture.original_picture.width,
            'height': picture.original_picture.height
        })
    img_url = 'pictures/' + picture.original_picture.name
    return render(request, 'picture.html', {
        'form': form,
        'img_url': img_url
    })

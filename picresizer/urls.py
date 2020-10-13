from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from picresizer import settings
from resizer.views import index, picture_upload, picture_resize

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('upload/', picture_upload),
    path('picture/<int:picture_id>', picture_resize),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

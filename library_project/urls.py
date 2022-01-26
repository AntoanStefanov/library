from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls'))
]

# showing images in browser/development -
# https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
# https://youtu.be/FdVuKt_iuSI?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&t=1248
# add only in dev, check docs for production mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

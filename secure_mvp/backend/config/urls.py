from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/projects/", include("apps.projects.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blockchain.urls")),
    path("accounts/", include("accounts.urls")),
    path("polls/", include("voting.urls")),
]
# static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

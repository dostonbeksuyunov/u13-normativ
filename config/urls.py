from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('', home_view, name='home'),
    path('books/', include('books.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]


# 🔥 MEDIA FIX (ENG MUHIM QISM)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


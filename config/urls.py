from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home_view, name='home'),

    path('books/', include('books.urls')),

    # 🔥 CUSTOM AUTH (register uchun)
    path('accounts/', include('accounts.urls')),

    # 🔥 DJANGO AUTH (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
]
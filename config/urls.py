from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect

def home_view(request):
    return render(request, 'home.html')  # templates/home.html

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('', home_view),  # bo'sh URL → home.html
]
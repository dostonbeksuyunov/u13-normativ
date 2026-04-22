from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home_view, name='home'),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
]
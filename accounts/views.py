
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import RegisterForm
from .forms import LoginForm

def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
        return redirect('home')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
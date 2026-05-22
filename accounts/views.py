from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm


# 🟢 REGISTER
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # 🔥 USER GROUPGA QO‘SHISH
            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)

            login(request, user)
            return redirect('book_list')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# 🟡 LOGIN
def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('book_list')

        form.add_error(None, "Username yoki password xato")

    return render(request, 'accounts/login.html', {'form': form})


# 🔴 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')
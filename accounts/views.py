from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    RestorePasswordForm
)

from .models import VerificationCode
from .utils import send_email_thread


# =========================
# REGISTER
# =========================
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)   # 🔥 FIX: email olish uchun

            # 🔥 MUHIM FIX: email saqlash
            user.email = form.cleaned_data.get('email')
            user.save()

            login(request, user)

            messages.success(
                request,
                'Muvaffaqiyatli ro‘yxatdan o‘tildi'
            )
            return redirect('home')

    return render(request, 'accounts/register.html', {'form': form})


# =========================
# LOGIN
# =========================
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            messages.success(request, 'Tizimga kirildi')
            return redirect('home')

    return render(request, 'accounts/login.html', {'form': form})


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)

    messages.success(request, 'Tizimdan chiqildi')
    return redirect('login')


# =========================
# FORGOT PASSWORD
# =========================
def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():

            username = form.cleaned_data['username']

            user = User.objects.filter(username=username).first()

            if not user:
                messages.error(request, 'Bunday user topilmadi')
                return redirect('forgot_password')

            # 🔥 MUHIM CHECK
            if not user.email:
                messages.error(request, 'Bu userda email yo‘q')
                return redirect('forgot_password')

            # eski code larni o‘chirish
            VerificationCode.objects.filter(user=user).delete()

            verification = VerificationCode.objects.create(user=user)

            subject = 'Parolni tiklash'
            message = f"""
Salom {user.username}

Sizning verification code:

{verification.code}

Code faqat 2 daqiqa ishlaydi.
"""

            send_email_thread(
                subject,
                message,
                [user.email]
            )

            messages.success(
                request,
                'Verification code emailingizga yuborildi'
            )

            return redirect('restore_password')

    return render(request, 'accounts/forgot_password.html', {'form': form})


# =========================
# RESTORE PASSWORD
# =========================
def restore_password_view(request):
    form = RestorePasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():

            verification = form.cleaned_data['verification']

            # 🔥 EXPIRATION CHECK (MUHIM)
            if verification.is_expired():
                verification.delete()
                messages.error(request, 'Code eskirgan. Qayta yuboring.')
                return redirect('forgot_password')

            user = verification.user

            new_password = form.cleaned_data['new_password']

            user.set_password(new_password)
            user.save()

            verification.delete()

            messages.success(request, 'Parol muvaffaqiyatli o‘zgardi')
            return redirect('login')

    return render(request, 'accounts/restore_password.html', {'form': form})

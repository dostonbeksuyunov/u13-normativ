from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import VerificationCode


# REGISTER
class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu email oldin ishlatilgan!")

        return email

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Parollar mos emas!")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user


# LOGIN
class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):

        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise ValidationError(
                "Login yoki parol noto‘g‘ri!"
            )

        cleaned_data['user'] = user

        return cleaned_data


# FORGOT PASSWORD
class ForgotPasswordForm(forms.Form):

    username = forms.CharField()


# RESTORE PASSWORD
class RestorePasswordForm(forms.Form):

    code = forms.IntegerField()

    new_password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):

        cleaned_data = super().clean()

        code = cleaned_data.get('code')

        new_password = cleaned_data.get('new_password')

        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if new_password != confirm_password:
            raise ValidationError(
                "Parollar mos emas!"
            )

        verification = VerificationCode.objects.filter(
            code=code
        ).order_by('-id').first()

        if not verification:
            raise ValidationError(
                "Code noto‘g‘ri!"
            )

        if verification.is_expired():
            raise ValidationError(
                "Code eskirib ketgan!"
            )

        cleaned_data['verification'] = verification

        return cleaned_data
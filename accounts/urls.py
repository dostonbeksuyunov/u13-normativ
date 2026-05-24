from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # FORGOT PASSWORD
    path(
        'forgot-password/',
        views.forgot_password_view,
        name='forgot_password'
    ),

    path(
        'restore-password/',
        views.restore_password_view,
        name='restore_password'
    ),
]
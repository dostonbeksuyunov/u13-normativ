from django.contrib import admin

from .models import VerificationCode


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'code',
        'expired_date',
        'created_at'
    )

    search_fields = (
        'user__username',
        'code'
    )

    list_filter = (
        'created_at',
    )
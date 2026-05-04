from django.contrib import admin
from .models import Book, Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(CartItem)
from django.contrib import admin
from .models import Book, Cart, CartItem, Order, OrderItem


# 📚 BOOK ADMIN
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price')
    search_fields = ('title', 'author')
    list_filter = ('author',)


# 🛒 CART ADMIN
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)


# 🧺 CART ITEM ADMIN
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'book', 'quantity')
    list_filter = ('cart',)


# 📦 ORDER ITEMS INLINE
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# 🧾 ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
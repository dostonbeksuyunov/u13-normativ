from django.urls import path
from . import views

urlpatterns = [
    # 📚 BOOKS
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/edit/', views.book_update, name='book_update'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),

    # 🛒 CART
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_item, name='increase_item'),
    path('cart/decrease/<int:item_id>/', views.decrease_item, name='decrease_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # 💳 ORDER
    path('checkout/', views.checkout, name='checkout'),
    path('my-books/', views.my_books, name='my_books'),
]
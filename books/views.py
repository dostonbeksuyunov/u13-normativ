from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Book, Cart, CartItem, Order, OrderItem


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 🛒 CART HELPER
def get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


# 📚 BOOK LIST
def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(is_deleted=False)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    paginator = Paginator(books.order_by('-id'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'query': query
    })


# 📚 CREATE
@login_required
def book_create(request):
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            price=request.POST['price'],
            description=request.POST.get('description', '')
        )
        return redirect('book_list')

    return render(request, 'books/book_form.html')


# ✏️ UPDATE
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.price = request.POST['price']
        book.description = request.POST.get('description', '')
        book.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'book': book})


# 🗑 DELETE
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.is_deleted = True
    book.save()
    return redirect('book_list')


# 🛒 ADD TO CART
@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart = get_cart(request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_view')


# 🧺 CART VIEW
@login_required
def cart_view(request):
    cart = get_cart(request.user)
    items = cart.items.select_related('book')

    total = sum(i.book.price * i.quantity for i in items)

    return render(request, 'books/cart.html', {
        'items': items,
        'total': total
    })


# ➕ INCREASE
@login_required
def increase_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart_view')


# ➖ DECREASE
@login_required
def decrease_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_view')


# ❌ REMOVE
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')


# 🧹 CLEAR CART
@login_required
def clear_cart(request):
    cart = get_cart(request.user)
    cart.items.all().delete()
    return redirect('cart_view')


# 💳 CHECKOUT (HAR USER O‘Z ORDERIGA EGA)
@login_required
def checkout(request):
    cart = get_cart(request.user)
    items = cart.items.select_related('book')

    if not items.exists():
        return redirect('cart_view')

    order = Order.objects.create(user=request.user)

    for item in items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )

    cart.items.all().delete()

    return redirect('my_books')


# 📖 MY BOOKS (USER-BASED ORDER)
@login_required
def my_books(request):
    orders = Order.objects.filter(user=request.user)\
        .prefetch_related('items__book')\
        .order_by('-created_at')

    return render(request, 'books/my_books.html', {
        'orders': orders
    })
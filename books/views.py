from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q

from .models import Book, Cart, CartItem, Order, OrderItem
from .forms import BookForm


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 🧠 CART HELPER
def get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


# 📚 BOOK LIST
@login_required
def book_list(request):

    query = request.GET.get('q', '')

    books = Book.objects.filter(is_deleted=False)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    return render(request, 'books/book_list.html', {
        'books': books.order_by('-id'),
        'query': query
    })


# 📖 BOOK DETAIL
@login_required
def book_detail(request, pk):

    book = get_object_or_404(
        Book,
        pk=pk,
        is_deleted=False
    )

    return render(request, 'books/book_detail.html', {
        'book': book
    })


# ➕ CREATE BOOK (ADMIN ONLY)
@login_required
@permission_required('books.add_book', raise_exception=True)
def book_create(request):

    form = BookForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {
        'form': form
    })


# ✏️ UPDATE BOOK (ADMIN ONLY)
@login_required
@permission_required('books.change_book', raise_exception=True)
def book_update(request, pk):

    book = get_object_or_404(Book, pk=pk)

    form = BookForm(
        request.POST or None,
        request.FILES or None,
        instance=book
    )

    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {
        'form': form
    })


# 🗑 DELETE BOOK (ADMIN ONLY)
@login_required
@permission_required('books.delete_book', raise_exception=True)
def book_delete(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.is_deleted = True
        book.save()

    return redirect('book_list')


# 🛒 ADD TO CART
@login_required
def add_to_cart(request, pk):

    book = get_object_or_404(Book, pk=pk)

    cart = get_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_view')


# 🧺 CART VIEW
@login_required
def cart_view(request):

    cart = get_cart(request.user)

    items = cart.items.select_related('book')

    total = sum(
        item.book.price * item.quantity
        for item in items
    )

    return render(request, 'books/cart.html', {
        'items': items,
        'total': total
    })


# ➕ INCREASE ITEM
@login_required
def increase_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart_view')


# ➖ DECREASE ITEM
@login_required
def decrease_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_view')


# ❌ REMOVE ITEM
@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('cart_view')


# 🧹 CLEAR CART
@login_required
def clear_cart(request):

    cart = get_cart(request.user)

    cart.items.all().delete()

    return redirect('cart_view')


# 💳 CHECKOUT
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


# 📦 MY ORDERS
@login_required
def my_books(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'books/my_books.html', {
        'orders': orders
    })
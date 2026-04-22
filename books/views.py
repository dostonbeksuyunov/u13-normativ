from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import BookForm


# =========================
# 📚 BOOK LIST + SEARCH
# =========================
@login_required(login_url='login')
def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'query': query
    })


# =========================
# ➕ CREATE (LOGIN REQUIRED)
# =========================
@login_required(login_url='login')
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {'form': form})


# =========================
# ✏️ UPDATE (LOGIN REQUIRED)
# =========================
@login_required(login_url='login')
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {'form': form})


# =========================
# ❌ DELETE (LOGIN REQUIRED)
# =========================
@login_required(login_url='login')
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        return redirect('book_list')

    return render(request, 'books/book_confirm_delete.html', {'book': book})


# =========================
# 🏠 HOME
# =========================
def home(request):
    return render(request, 'home.html')


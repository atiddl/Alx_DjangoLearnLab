from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .forms import BookSearchForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from .forms import ExampleForm
# View books (can_view permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    form = BookSearchForm(request.GET or None)

    if form.is_valid():
        query = form.cleaned_data['query']
        books = books.filter(title__icontains=query)

    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})

# Create book (can_create permission)
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Edit book (can_edit permission)
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Delete book (can_delete permission)
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


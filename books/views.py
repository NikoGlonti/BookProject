from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render

from books.models import Author, Book, Publisher, Store


def home(request):
    return render(request, 'home.html')


def author(request):
    author_list = Author.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    return render(request, 'author_ls.html', {'author_list': author_list})


def author_inf(request, pk):
    author_info = get_object_or_404(Author.objects.prefetch_related
                                    ('book_set').annotate(average_rating=Round(Avg('book__rating'))), pk=pk)
    return render(request, 'author_inf.html', {'author_info': author_info})


def book(request):
    book_list = Book.objects.all()
    return render(request, 'book_ls.html', {'book_list': book_list})


def book_inf(request, pk):
    books_info = get_object_or_404(Book, pk=pk)
    return render(request, 'book_inf.html', {'books_info': books_info})


def publisher(request):
    publisher_list = Publisher.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    return render(request, 'publisher.html', {'publisher_list': publisher_list})


def publisher_inf(request, pk):
    publishers_info = get_object_or_404(Publisher.objects.all()
                                        .prefetch_related('book_set').annotate(books_count=Count('book')), pk=pk)
    return render(request, 'publisher_inf.html', {'publishers_info': publishers_info})


def store(request):
    store_list = Store.objects.all().prefetch_related('books').annotate(books_count=Count('books'))
    return render(request, 'store_ls.html', {'store_list': store_list})


def store_inf(request, pk):
    stores_info = get_object_or_404(Store.objects.all().prefetch_related('books'), pk=pk)
    return render(request, "store_inf.html", {'stores_info': stores_info})

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from books.models import Author, Book, Publisher, Store
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView


# def home(request):
#     return render(request, 'home.html')
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        context['num_authors'] = Author.objects.count()
        context['num_publishers'] = Publisher.objects.count()
        context['num_stores'] = Store.objects.count()
        return context


@cache_page(10)
def author(request):
    author_list = Author.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    return render(request, 'author_ls.html', {'author_list': author_list})


@cache_page(10)
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


@cache_page(10)
def publisher(request):
    publisher_list = Publisher.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    return render(request, 'publisher.html', {'publisher_list': publisher_list})


def publisher_inf(request, pk):
    publishers_info = get_object_or_404(Publisher.objects.all()
                                        .prefetch_related('book_set').annotate(books_count=Count('book')), pk=pk)
    return render(request, 'publisher_inf.html', {'publishers_info': publishers_info})


@cache_page(10)
def store(request):
    store_list = Store.objects.all().prefetch_related('books').annotate(books_count=Count('books'))
    return render(request, 'store_ls.html', {'store_list': store_list})


def store_inf(request, pk):
    stores_info = get_object_or_404(Store.objects.all().prefetch_related('books'), pk=pk)
    return render(request, "store_inf.html", {'stores_info': stores_info})


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'create_book.html'
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    success_url = reverse_lazy('book:book')
    login_url = '/admin/login/'


class BookUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'book_update.html'
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    login_url = '/admin/login/'

    def get_success_url(self):
        book_id = self.kwargs['pk']
        return reverse_lazy('book:book-update', kwargs={'pk': book_id})


class BookDelete(LoginRequiredMixin, DeleteView, ):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('book:book')
    login_url = '/admin/login/'


@method_decorator(cache_page(10), name='dispatch')
class BookDetail(DetailView):
    model = Book
    template_name = 'book_inf.html'


@method_decorator(cache_page(10), name='dispatch')
class BookList(ListView):
    model = Book
    template_name = 'book_ls.html'
    paginate_by = 500
    queryset = Book.objects.annotate(num_authors=Count('authors')).select_related('publisher')
    context_object_name = 'books'

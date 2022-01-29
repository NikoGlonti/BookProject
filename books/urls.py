from . import views
from django.urls import path

from books.views import *

app_name = 'book'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('author/', author, name='author'),
    path('author/<int:pk>', author_inf, name='author-detail'),
    path('book/', book, name='book'),
    path('book/<int:pk>', book_inf, name='book-detail'),
    path('publisher/', publisher, name='publishers'),
    path('publisher/<int:pk>', publisher_inf, name='publisher-detail'),
    path('store/', store, name='stores'),
    path('store/<int:pk>', store_inf, name='store-detail'),

    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/delete/<int:pk>/', views.BookDelete.as_view(), name='book-delete'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='books_detail'),
    path('book/', views.BookList.as_view(), name='books'),

]

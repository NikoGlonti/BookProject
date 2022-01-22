from . import views
from django.urls import path

from books.views import *
app_name = 'book'
urlpatterns = [
    path('', views.home, name='home'),
    path('author/', author, name='author'),
    path('author/<int:pk>', author_inf, name='author-detail'),
    path('book/', book, name='book'),
    path('book/<int:pk>', book_inf, name='book-detail'),
    path('publisher/', publisher, name='publishers'),
    path('publisher/<int:pk>', publisher_inf, name='publisher-detail'),
    path('store/', store, name='stores'),
    path('store/<int:pk>', store_inf, name='store-detail'),
]

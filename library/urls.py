from django.urls import path
from .views import (
    AuthorCreateView,
    AuthorUpdateView,
    AuthorListView,
    BookDetailView,
    BookUpdateView,
    BookCreateView,
    BookDeleteView,
    BooksListView,
    RecommendBookView,
    ReviewBookView,
)

app_name = 'library'

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='authors_list'),
    path('author/new/', AuthorCreateView.as_view(), name='create_author'),
    path('author/update/<int:pk>/', AuthorUpdateView.as_view(), name='update_author'),

    path('books/', BooksListView.as_view(), name='books_list'),
    path('book/new/', BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('book/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('book/review/<int:pk>/', ReviewBookView.as_view(), name='book_review'),
    path('book/recommend/<int:pk>/', RecommendBookView.as_view(), name='book_recommend'),
]

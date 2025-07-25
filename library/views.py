from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from .models import Book, Author
from .services import BookService

from library.forms import BookForm, AuthorForm


class AuthorListView(ListView):
    """
        Отображение списка всех авторов.
    """

    model = Author
    template_name = 'library/authors_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        queryset = cache.get('authors_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('authors_queryset', queryset, 60 * 15)
        return queryset


class AuthorCreateView(CreateView):
    """
        Класс для создания автора.
    """

    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:authors_list')


class AuthorUpdateView(UpdateView):
    """
        Класс для обновления информации об автора.
    """

    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:authors_list')


@method_decorator(cache_page(60 * 15), name='dispatch')  # Высокоуровневое кэширование
class BooksListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
        Отображение данных в шаблоне.
    """

    model = Book
    template_name = 'library/books_list.html'
    context_object_name = 'books'
    permission_required = 'library.view_book'

    def get_queryset(self):
        """
            Фильтрация отображаемых данных в шаблоне.
        """
        queryset = super().get_queryset()
        return queryset.filter(publication_date__year__gt=1000)


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
        Создание книги.
    """

    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:books_list')
    permission_required = 'library.add_book'


@method_decorator(cache_page(60 * 15), name='dispatch')
class BookDetailView(LoginRequiredMixin, DetailView):
    """
        Детальная информация об объекте.
    """

    model = Book
    template_name = 'library/books_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        """
            Метод для расширения контекста.
        """
        book_id = self.object.id
        context = super().get_context_data(**kwargs)
        context['author_books_count'] = Book.objects.filter(author=self.object.author).count()
        context['average_rating'] = BookService.calculate_average_rating(book_id)
        context['is_popular'] = BookService.is_popular(book_id)

        return context


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
        Обновление информации о книге.
    """

    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:books_list')
    permission_required = 'library.change_book'


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
        Удаление книги.
    """

    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('library:books_list')
    permission_required = 'library.delete_book'


class ReviewBookView(LoginRequiredMixin, View):
    """
        Проверка прав доступа пользователя на просмотр книги.
    """

    def post(self, request, pk):
        """
            Обработка post запроса.
        """
        book = get_object_or_404(Book, pk=pk)
        if not request.user.has_perm('library.can_review_book'):
            return HttpResponseForbidden('У вас нет права для рецензирования книги')
        else:
            book.review = request.POST.get('review')
            book.save()
            return redirect('library:book_detail', pk=pk)


class RecommendBookView(LoginRequiredMixin, View):
    """
        Проверка прав доступа пользователя для рекомендации книги.
    """

    def post(self, request, pk):
        """
            Обработка post запроса.
        """
        book = get_object_or_404(Book, pk=pk)
        if not request.user.has_perm('library.can_recommend_book'):
            return HttpResponseForbidden('У вас нет права для рекомендации книги')
        book.recommend = True
        book.save()
        return redirect('library:book_detail', pk=pk)

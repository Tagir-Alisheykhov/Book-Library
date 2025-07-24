from django import forms
from .models import Book, Author


class AuthorForm(forms.ModelForm):
    """
        Создание формы для автора. По атрибутам модели
    """
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'birth_date',]


class BookForm(forms.ModelForm):
    """
        Создание формы для автора. По атрибутам модели
    """
    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'author',]


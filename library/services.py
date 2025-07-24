from .models import Book, Review


class BookService:
    """ Класс для сервисного слоя """

    @staticmethod
    def calculate_average_rating(book_id):
        """
            Вычисление средней оценки книги.
            :param book_id: Текущая книга
            :return: Средняя оценка книги
        """
        reviews = Review.objects.filter(book_id=book_id)
        if not reviews.exists():
            return None
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / reviews.count()
        return average_rating

    @staticmethod
    def is_popular(book_id, threshold=4):
        """
            Определение того, является ли книга популярной.
            :param book_id: Текущая книга
            :param threshold: Минимальное значение для определения того,
            является ли книга популярной.
            :return: Булево значение
        """
        average_rating = BookService.calculate_average_rating(book_id)
        if average_rating is None:
            return None
        return average_rating >= threshold

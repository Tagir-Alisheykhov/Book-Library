from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
        pass
    """

    def handle(self, *args, **options):
        """
            pass
            :param args:
            :param options:
            :return:
        """

        User = get_user_model()
        user = User.objects.create(
            email='testadmin@sky.pro',
            first_name='Admin',
            last_name='Admin',
            # password='1234' - так пароль н будет работать.
        )

        # Пароль нужно хэшировать:
        user.set_password('1234')

        # Перед сохранением:
        # Указываем для пользователя статус персонала:
        user.is_staff = True
        # Даем все права пользователю:
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created admin user with email {user.email}!')
        )


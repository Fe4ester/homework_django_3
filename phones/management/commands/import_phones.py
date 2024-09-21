import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Импорт данных из CSV файла в модель Phone'

    def add_arguments(self, parser):
        # Можешь добавить дополнительные аргументы команды, если потребуется
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # Генерация slug из имени телефона
            phone_slug = slugify(phone['name'])

            # Создание или обновление объекта Phone
            Phone.objects.update_or_create(
                id=phone['id'],  # Используем id из файла CSV
                defaults={
                    'name': phone['name'],
                    'image': phone['image'],
                    'price': float(phone['price']),
                    'release_date': phone['release_date'],
                    'lte_exists': phone['lte_exists'].strip().lower() == 'true',
                    'slug': phone_slug,
                }
            )

        self.stdout.write(self.style.SUCCESS('Телефоны успешно импортированы'))

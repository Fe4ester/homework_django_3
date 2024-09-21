import os
import django
import csv
from django.utils.text import slugify

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from phones.models import Phone

def import_phones():
    file_path = os.path.join(os.path.dirname(__file__), 'phones.csv')

    # Открываем CSV файл
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                try:
                    phone, created = Phone.objects.update_or_create(
                        id=row['id'],
                        defaults={
                            'name': row['name'],
                            'image': row['image'],
                            'price': float(row['price']),
                            'release_date': row['release_date'],
                            'lte_exists': row['lte_exists'].strip().lower() == 'true',
                            'slug': slugify(row['name'])
                        }
                    )
                    if created:
                        print(f'Добавлен новый телефон: {phone.name}')
                    else:
                        print(f'Обновлен телефон: {phone.name}')
                except Exception as e:
                    print(f'Ошибка при обработке телефона {row["name"]}: {str(e)}')
    except FileNotFoundError:
        print(f'Файл {file_path} не найден. Убедитесь, что файл существует.')

if __name__ == '__main__':
    import_phones()

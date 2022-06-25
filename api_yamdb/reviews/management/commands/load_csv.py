import csv

from django.core.management import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User
)


class Command(BaseCommand):
    help = 'Заполняет базу данных контентом из csv-файлов'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def import_users(self, directory):
        with open(directory + 'users.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    User(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        bio=row['bio'],
                        role=row['role'],
                    )
                )
            User.objects.bulk_create(temp_data)

    def import_categories(self, directory):
        with open(directory + 'category.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    Category(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug']
                    )
                )
            Category.objects.bulk_create(temp_data)

    def import_genres(self, directory):
        with open(directory + 'genre.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    Genre(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug']
                    )
                )
            Genre.objects.bulk_create(temp_data)

    def import_titles(self, directory):
        with open(directory + 'titles.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    Title(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=Category.objects.get(id=row['category'])
                    )
                )
            Title.objects.bulk_create(temp_data)

    def import_reviews(self, directory):
        with open(directory + 'review.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    Review(
                        id=row['id'],
                        title=Title.objects.get(id=row['title_id']),
                        text=row['text'],
                        score=row['score'],
                        author=User.objects.get(id=row['author']),
                        pub_date=row['pub_date']
                    )
                )
            Review.objects.bulk_create(temp_data)

    def import_comments(self, directory):
        with open(directory + 'comments.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    Comment(
                        id=row['id'],
                        text=row['text'],
                        author=User.objects.get(id=row['author']),
                        review=Review.objects.get(id=row['review_id']),
                        pub_date=row['pub_date']
                    )
                )
            Comment.objects.bulk_create(temp_data)

    def import_genres_titles(self, directory):
        with open(directory + 'genre_title.csv', 'r', encoding='UTF-8') as df:
            temp_data = []
            reader = csv.DictReader(df)
            for row in reader:
                temp_data.append(
                    GenreTitle(
                        id=row['id'],
                        genre=Genre.objects.get(id=row['genre_id']),
                        title=Title.objects.get(id=row['title_id'])
                    )
                )
            GenreTitle.objects.bulk_create(temp_data)

    def handle(self, *args, **options):
        directory = options['file_path']
        self.import_users(directory)
        self.import_categories(directory)
        self.import_genres(directory)
        self.import_titles(directory)
        self.import_reviews(directory)
        self.import_comments(directory)
        self.import_genres_titles(directory)
        self.stdout.write(self.style.SUCCESS('Импорт данных завершен'))

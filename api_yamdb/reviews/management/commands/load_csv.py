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

PROGRAM_FAILURE = 'Ошибка при импорте данных {}: {}'


class Command(BaseCommand):
    help = 'Заполняет базу данных контентом из csv-файлов'

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        directory = options["file_path"]
        try:
            with open(directory + 'users.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
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
        except Exception as err:
            print(PROGRAM_FAILURE.format('User', err))

        try:
            with open(directory + 'category.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
                for row in reader:
                    temp_data.append(
                        Category(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug']
                        )
                    )
                Category.objects.bulk_create(temp_data)
        except Exception as err:
            print(PROGRAM_FAILURE.format('Category', err))

        try:
            with open(directory + 'genre.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
                for row in reader:
                    temp_data.append(
                        Genre(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug']
                        )
                    )
                Genre.objects.bulk_create(temp_data)
        except Exception as err:
            print(PROGRAM_FAILURE.format('Genre', err))

        try:
            with open(directory + 'titles.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
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
        except Exception as err:
            print(PROGRAM_FAILURE.format('Title', err))

        try:
            with open(directory + 'review.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
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
        except Exception as err:
            print(PROGRAM_FAILURE.format('Review', err))

        try:
            with open(directory + 'comments.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
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
        except Exception as err:
            print(PROGRAM_FAILURE.format('Comment', err))

        try:
            with open(directory + 'genre_title.csv') as datafile:
                temp_data = []
                reader = csv.DictReader(datafile)
                for row in reader:
                    temp_data.append(
                        GenreTitle(
                            id=row['id'],
                            genre=Genre.objects.get(id=row['genre_id']),
                            title=Title.objects.get(id=row['title_id'])
                        )
                    )
                GenreTitle.objects.bulk_create(temp_data)
        except Exception as err:
            print(PROGRAM_FAILURE.format('GenreTitle', err))
        self.stdout.write(
            self.style.SUCCESS('Импорт данных завершен')
        )

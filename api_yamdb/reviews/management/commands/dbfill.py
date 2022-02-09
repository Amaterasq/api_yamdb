from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

import csv

from reviews.models import (User, Category, Title, Review, Genre,
                            GenreTitle, Comment)


class Command(BaseCommand):
    """Management-команда наполняющей базу данных тестовыми данными
    из каталога /api_yamdb/static/data.
    """
    help = ('Helps to fill the database with test '
            'data from "/api_yamdb/static/data"')

    def fill_table_users(self):
        self.stdout.write(
            '/api_yamdb/static/data/users.csv', ending=' .... '
        )
        try:
            with open('static/data/users.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        User.objects.get_or_create(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6],
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def fill_table_category(self):
        self.stdout.write(
            '/api_yamdb/static/data/category.csv', ending=' .... '
        )
        try:
            with open('static/data/category.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Category.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def fill_table_titles(self):
        self.stdout.write(
            '/api_yamdb/static/data/titles.csv', ending=' .... '
        )
        try:
            with open('static/data/titles.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Title.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=get_object_or_404(Category, id=row[3])
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def fill_table_review(self):
        self.stdout.write(
            '/api_yamdb/static/data/review.csv', ending=' .... '
        )
        try:
            with open('static/data/review.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Review.objects.get_or_create(
                            id=row[0],
                            title_id=row[1],
                            text=row[2],
                            author=get_object_or_404(User, id=row[3]),
                            score=row[4],
                            pub_date=row[5]
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def fill_table_genre(self):
        self.stdout.write(
            '/api_yamdb/static/data/genre.csv', ending=' .... '
        )
        try:
            with open('static/data/genre.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Genre.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def fill_table_genre_title(self):
        self.stdout.write(
            '/api_yamdb/static/data/genre_title.csv', ending=' .... '
        )
        try:
            with open(
                'static/data/genre_title.csv', encoding='utf-8'
            ) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        GenreTitle.objects.get_or_create(
                            id=row[0],
                            title_id=get_object_or_404(Title, id=row[1]),
                            genre_id=get_object_or_404(Genre, id=row[2])
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def fill_table_comments(self):
        self.stdout.write(
            '/api_yamdb/static/data/comments.csv', ending=' .... '
        )
        try:
            with open('static/data/comments.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Comment.objects.get_or_create(
                            id=row[0],
                            review_id=get_object_or_404(Review, id=row[1]),
                            text=row[2],
                            author=get_object_or_404(User, id=row[3]),
                            pub_date=row[4]
                        )
            return self.stdout.write(self.style.SUCCESS('OK'))
        except Exception as error:
            self.stdout.write('FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def handle(self, *args, **options):
        self.stdout.write(
            '\nStarting to fill the database with test data:\n\n'
        )
        try:
            self.fill_table_users()
            self.fill_table_category()
            self.fill_table_titles()
            self.fill_table_review()
            self.fill_table_genre()
            self.fill_table_genre_title()
            self.fill_table_comments()
            self.stdout.write(
                '\nThe database has been successfully filled with test data!'
            )
        except Exception as error:
            self.stderr.write(
                f'Execution error - {error}!'
            )

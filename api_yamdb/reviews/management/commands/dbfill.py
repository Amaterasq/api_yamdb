from django.core.management.base import BaseCommand

import csv

from reviews.models import Category, Comments


class Command(BaseCommand):
    """Management-команда наполняющей базу данных тестовыми данными
    из каталога /api_yamdb/static/data.
    """
    help = ('Helps to fill the database with test '
            'data from "/api_yamdb/static/data"')
    titles_list = ('category', 'comments', 'genre_title',
                   'genre', 'review', 'titles', 'users',)

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', nargs='?', type=str, default=None
        )

    def parse_test_data(self, titles):
        self.stdout.write(
            f'Work with files: {titles}'
        )
        for title in titles:
            with open(f'static/data/{title}.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                # column_names = []
                # column_count = 0
                # row_count = 0
                # for line_num, line in enumerate(reader):
                #     if line_num == 0:
                #         for i in range(len(line)):
                #             column_names.append(line[i])
                #         column_count = len(line)
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    if title == 'category':
                        Category.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2],
                        )
                    elif title == 'comments':
                        Comments.objects.get_or_create(
                            id=row[0],
                            review_id=row[1],
                            text=row[2],
                            author=row[3],
                            pub_date=row[4]
                        )
                # self.stdout.write(
                #     f'Столбцы: {column_names}, количество столбцов: {column_count}, количество записей: {row_count}'
                # )

    def handle(self, *args, **options):
        if options['file_name'] is None:
            self.parse_test_data(self.titles_list)
        else:
            file_name = (options['file_name'],)
            self.parse_test_data(file_name)
        self.stdout.write(
            'Filling the database with test data was successful!'
        )

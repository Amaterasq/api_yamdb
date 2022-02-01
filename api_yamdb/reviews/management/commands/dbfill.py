from django.core.management.base import BaseCommand

import csv


class Command(BaseCommand):
    """Management-команда наполняющей базу данных тестовыми данными
    из каталога /api_yamdb/static/data.
    """
    help = ('Helps to fill the database with test '
            'data from "/api_yamdb/static/data"')
    titles_list = ('category.csv', 'comments.csv', 'genre_title.csv',
                   'genre.csv', 'review.csv', 'titles.csv', 'users.csv',)

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', nargs='?', type=str, default=None
        )

    def parse_test_data(self, titles):
        self.stdout.write(
            f'Work with files: {titles}'
        )
        data = []
        for title in titles:
            with open(f'static/data/{title}', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row[0])
                    data.append(row[1])
                    data.append(row[2])
        self.stdout.write(f'Read Data: {data}')

    def handle(self, *args, **options):
        if options['file_name'] is None:
            self.parse_test_data(self.titles_list)
        else:
            file_name = (options['file_name'],)
            self.parse_test_data(file_name)
        self.stdout.write(
            'Filling the database with test data was successful!'
        )

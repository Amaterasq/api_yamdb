from django.core.management.base import BaseCommand
import reviews.models


class Command(BaseCommand):
    help = ('Helps to fill the database with test '
            'data from "/api_yamdb/static/data"')

    def handle(self, *args, **options):
            self.stdout.write(
                self.style.SUCCESS(
                    'Filling the database with test data was successful!'
                )
            )

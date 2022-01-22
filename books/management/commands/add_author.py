import random

from django.core.management.base import BaseCommand

from faker import Faker

from books.models import Author


class Command(BaseCommand):
    help = 'Creation of authors. You must enter the quantity'

    def add_arguments(self, parser):
        parser.add_argument('add_authors', type=int, choices=range(1, 100000), help='number of authors')

    def handle(self, *args, **options):
        for _ in range(options['add_authors']):
            Author.objects.create(name=Faker().name(), age=random.randint(15, 98))
            self.stdout.write(self.style.SUCCESS('Successfully added author "%s, %s"' % (Author.objects.last().name,
                                                                                         Author.objects.last().age)))

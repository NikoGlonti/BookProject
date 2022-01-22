import os
import random

from django.core.management.base import BaseCommand

from faker import Faker

from books.models import Author, Book, Publisher


def create_title():
    title_start = ['Fantasy', 'Adventure', 'Novel', 'Historical', 'Horror',
                   'Detective']
    title = title_start[random.randint(0, len(title_start) - 1)]
    rand_month = Faker().date_between(start_date='-130y', end_date='-15y').strftime("%B")
    return f'{title} {Faker().name()}' if title != title_start[1] and title_start[2] else f'{title} {rand_month}'


def get_authors():
    authors = []
    if Author.objects.all().count() < 3:
        BaseCommand().stdout.write(BaseCommand().style.ERROR('Empty Author table in db'))
        BaseCommand().stdout.write(BaseCommand().style.SUCCESS('Creating 3 new Author objects'))
        os.system(f'python manage.py add_authors {3 - Author.objects.all().count()}')
    for i in range(random.randint(1, 3)):
        authors.append(
            Author.objects.get(
                pk=Author.objects.all().values_list('pk', flat=True)
                [random.randint(0,
                                len(Author.objects.all().values_list(
                                    'pk',
                                    flat=True)) - 1)]))
    return set(authors)


def get_publisher():
    if Publisher.objects.all().count() == 0:
        BaseCommand().stdout.write(BaseCommand().style.ERROR('Empty Publisher table in db'))
        BaseCommand().stdout.write(BaseCommand().style.SUCCESS('Creating Publisher '))
        os.system('python manage.py add_publishers 1')
    publisher = Publisher.objects.get(
        pk=Publisher.objects.all().values_list('pk', flat=True)
        [random.randint(0,
                        len(Publisher.objects.all().values_list(
                            'pk',
                            flat=True)) - 1)])
    return publisher


class Command(BaseCommand):
    help = 'Creates  number of new books. You specify a number'

    def add_arguments(self, parser):
        parser.add_argument('add_books', type=int, choices=range(1, 100000), help='Value of the created ')

    def handle(self, *args, **options):
        for _ in range(options['add_books']):
            Book.objects.create(name=create_title(),
                                pages=random.randint(100, 3000),
                                price=round(random.uniform(10, 60), 2),
                                rating=round(random.uniform(0, 5), 2),
                                publisher=get_publisher(),
                                pubdate=Faker().date_between(start_date='-130y', end_date='-15y')
                                )
            authors = get_authors()
            for author in authors:
                Book.objects.last().authors.add(author)

            self.stdout.write(self.style.SUCCESS(f'Successfully added book {Book.objects.last().name}'))

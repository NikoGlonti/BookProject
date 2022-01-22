from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Test filling of the database'

    def add_arguments(self, parser):
        parser.add_argument('authors', nargs='?', type=int, choices=range(1, 100000), default=25,
                            help='range(1, 100000)')
        parser.add_argument('publishers', nargs='?', type=int, choices=range(1, 100000), default=5,
                            help='range(1, 100000)')
        parser.add_argument('books', nargs='?', type=int, choices=range(1, 100000), default=100,
                            help='range(1, 100000)')
        parser.add_argument('stores', nargs='?', type=int, choices=range(1, 100000), default=47,
                            help='range(1, 100000)')

    def handle(self, *args, **options):
        call_command("add_author", options['author'])
        call_command("add_publisher", options['publisher'])
        call_command("add_book", options['books'])
        call_command("add_stores", options['stores'])

        self.stdout.write(self.style.SUCCESS('Database full'))



from django.core.management.base import BaseCommand, CommandError
from scraping.tests.factories import company


class Command(BaseCommand):
    help = 'Fill up the database by fake data'

    def add_arguments(self, parser):
        parser.add_argument('companies', type=int, help='Indicates the number of companies to be created')

    def handle(self, *args, **options):

        for number in range(options['companies']):
            try:
                new_company = company.CompanyFactory()
                for _ in range(2):
                    company.EmployeeFactory( company=new_company)

            except Exception as e:
                raise CommandError(f'Error occur: {e}')

        self.stdout.write(self.style.SUCCESS(f'{options["companies"]} successfully created companies with employees'))

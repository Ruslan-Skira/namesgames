import random

from django.core.management.base import BaseCommand, CommandError

from accounts.tests.factories.user_factory import UserFactory
from company.tests.factories.company_factory import CompanyFactory

#TODO create less users 1 company owner and 5 Employees
class Command(BaseCommand):
    help = 'Fill up the database by fake data'

    def add_arguments(self, parser):
        parser.add_argument('companies', type=int, help='Indicates the number of companies to be created')

    def handle(self, *args, **options):

        for number in range(options['companies']):
            try:
                new_company = CompanyFactory()
                for _ in range(random.randint(1, 17)):
                    UserFactory(company=new_company)
            except Exception as e:
                raise CommandError(f'Error occur: {e}')

        self.stdout.write(self.style.SUCCESS(f'{options["companies"]} successfully created companies with employees'))
# TODO make other file with command drop all db.To clear all data and fill up it again.

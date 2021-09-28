import random

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from accounts.tests.factories.user_factory import EmployeeFactory
from company.tests.factories.company_factory import CompanyFactory


class Command(BaseCommand):
    """
    Command create fake company, owner and 1-25 employees.
    """

    help = 'Fill up the database by fake data'

    def add_arguments(self, parser):
        parser.add_argument('companies', type=int, help='Indicates the number of companies to be created')

    def handle(self, *args, **options):

        for number in range(options['companies']):
            try:
                new_company = CompanyFactory()
                EmployeeFactory(company=new_company, is_company_owner=True)
                for _ in range(random.randint(1, 25)):
                    EmployeeFactory(company=new_company, is_company_owner=False)
            except Exception as e:
                raise CommandError(f'Error occur: {e}')

        self.stdout.write(self.style.SUCCESS(f'{options["companies"]} successfully created companies with employees'))

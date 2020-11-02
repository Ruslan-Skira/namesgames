import datetime

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from company.models import Company, Employee
from company.serializers import CompanySerializer

# initialize APIClient app
client = Client()


class GetCompanyTest(TestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        self.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        self.test_company2 = Company.objects.create(
            name='TestCompanyAPI2', last_parsed_at=datetime.datetime.today())
        Employee.objects.create(
            first_name='test_name', last_name='test_last_name', picture_url='http://fakeurl', position='test_position',
            profile_url='http://profile_url',
            birthday=datetime.date(2000, 12, 1), email='example@test.com', phone_number='+3809877612', skype='test',
            company=self.test_company)

    def test_get_all_companies(self):
        # get API response
        response = client.get(reverse('companies'))
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_company(self):
        response = client.get(
            reverse('company', kwargs={'slug': self.test_company.slug}))
        company = Company.objects.get(slug=self.test_company.slug)
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_company(self):
        response = client.get(
            reverse('company', kwargs={'slug': 'guffy_fail_slug'}
                    ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_session(self):
        """Test for testing the user session"""
        # TODO clarify why 3 company in the session why not 2?
        client.get(
            reverse('company', kwargs={'slug': self.test_company.slug}))
        client.get(
            reverse('company', kwargs={'slug': self.test_company2.slug}))

        print(client.session['company_visited'])
        self.assertEqual(len(client.session['company_visited']), 3)

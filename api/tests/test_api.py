from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .. models import Apartment

# Apartment create and list test
from ..serializers import ApartmentDetailSerializer


class ApartmentTestCase(APITestCase):
    def test_post(self):
        apartment_1 = Apartment.objects.create(document='Доверенность', room_count=1, apartment_type='Пентхаус',
                                               apartment_status='Требует ремонта', apartment_area=21.0,
                                               kitchen_area=11.0, loggia=1, heating_type='Газ', commission=112,
                                               description='test description', price=123213,
                                               address='Test address', apart_class='Студия, санузел', is_actual=0,
                                               created_date='2021-07-07 04:34:23.861943', owner_id=None)
        url = reverse('apartment-list')
        print(url)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_detail(self):
        apartment_1 = Apartment.objects.create(document='Доверенность', room_count=1, apartment_type='Пентхаус',
                                               apartment_status='Требует ремонта', apartment_area=21.0,
                                               kitchen_area=11.0, loggia=1, heating_type='Газ', commission=112,
                                               description='test description', price=123213,
                                               address='Test address', apart_class='Студия, санузел', is_actual=0,
                                               created_date='2021-07-07 04:34:23.861943', owner_id=None)
        url = '/api/apartment/1/'
        print(url)
        response = self.client.get(url)
        serialized_data = ApartmentDetailSerializer(apartment_1).data
        self.assertEqual(serialized_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)



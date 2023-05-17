from django.contrib.auth.models import User
from .models import Pet
from rest_framework import status
from rest_framework.test import APITestCase


class PetListViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='pass')
    
    def test_can_list_pets(self):
        user = User.objects.get(username='test')
        Pet.objects.create(owner=user, name='Luna')
        response = self.client.get('/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_pet(self):
        data = {
            'name': 'Luna',
            'pet_type': 'Cat',
        }
        self.client.login(username='test', password='pass')
        response = self.client.post('/pets/', data, format='multipart')
        count = Pet.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Luna')
        self.assertEqual(response.data['pet_type'], 'Cat')
        self.assertEqual(count, 1)

    # def test_create_pet_unauthenticated(self):
    #     url = '/pets/'
    #     data = {
    #         'name': 'Fluffy',
    #         'pet_type': 'Cat',
    #         'image': '<image-data>',
    #         'about': 'A cute cat'
    #     }
    #     self.client.force_authenticate(user=None)
    #     response = self.client.post(url, data, format='multipart')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_create_pet_invalid_data(self):
    #     url = '/pets/'
    #     data = {
    #         'name': '',  # Invalid name (empty)
    #         'pet_type': 'Cat',
    #         'image': '<image-data>',
    #         'about': 'A cute cat'
    #     }
    #     response = self.client.post(url, data, format='multipart')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('name', response.data)

    # def test_retrieve_pets(self):
    #     url = '/pets/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Add more assertions to verify the response data

    # def test_retrieve_specific_pet(self):
    #     pet = Pet.objects.create(owner=self.user, name='Fluffy', pet_type='Cat')
    #     url = f'/pets/{pet.pk}/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'Fluffy')

    # def test_retrieve_pet_unauthenticated(self):
    #     pet = Pet.objects.create(owner=self.user, name='Fluffy', pet_type='Cat')
    #     url = f'/pets/{pet.pk}/'
    #     self.client.force_authenticate(user=None)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_retrieve_pet_by_owner(self):
    #     pet = Pet.objects.create(owner=self.user, name='Fluffy', pet_type='Cat')
    #     url = f'/pets/{pet.pk}/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['owner'], self.user.username)
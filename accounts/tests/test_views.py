from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .factories.accounts import UserFactory
from django.urls import reverse
from rest_framework import status


class TestAccountsApp(TestCase):

  def setUp(self):
    self.client = APIClient()
    self.user = UserFactory()
  
  def test_registering_user(self):
    register_data = {
      "email": "testing@gmail.com",
      "password": "test@123",
      "name": "test",
      "phone": "9872721212",
      "date_of_birth": "1993-04-20",
      "user_type": "CUSTOMER"
    }

    inv_register_data = {
      "email": "testing@gmail.com",
    }

    response = self.client.post(reverse('register'), inv_register_data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    response = self.client.post(reverse('register'), register_data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertContains(response, register_data['email'])

  def test_login_fetch_token(self):
    response = self.client.post(reverse('token_obtain_pair'), \
               {"email":self.user.email, "password":"test@12"})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    response = self.client.post(reverse('token_obtain_pair'), \
               {"email":self.user.email, "password":"test@123"})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIsNotNone(response.data['access'])
    self.assertIsNotNone(response.data['userdata'])

  def test_updating_user_profile(self):
    # update without authenticating
    response = self.client.put(reverse('updated_user_profile', \
                                       kwargs={'id':self.user.id}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # update after loggin in
    response = self.client.post(reverse('token_obtain_pair'), \
            {"email":self.user.email, "password":"test@123"})
    token = response.data['access']
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {token}")
    response = self.client.put(reverse('updated_user_profile', \
                   kwargs={'id':self.user.id}), {"name":"test2"})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["userdata"]["name"], "test2")



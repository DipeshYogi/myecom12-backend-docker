from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .factories.orderapp import CustomerFactory, ShopkeeperFactory, \
                                ECHFactory, ECLFactory
from ..models import ECH, ECL


class TestOrderApp(TestCase):
  """
    Test Cases for Order app
  """

  def setUp(self):
    self.client = APIClient()
    self.cust = CustomerFactory()
    self.shop = ShopkeeperFactory()
    self.ech = ECHFactory(HCUST=self.cust, HSHOP=self.shop)
    self.ecl1 = ECLFactory(LORD=self.ech)
    self.ecl2 = ECLFactory(LORD=self.ech)

  def test_fetching_shop_orders(self):
    # fetch shop order without authentication
    response = self.client.get(reverse('shop_order'))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # fetch shop order with authentication
    response = self.client.post(reverse("token_obtain_pair"), \
               {"email":self.shop.email, "password":"test@123"}, \
               format="json")
    token = response.data["access"]
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')
    response = self.client.get(reverse('shop_order'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertContains(response, self.ech)
  
  def test_fetching_shoporder_details(self):
    # fetch shop order lines without authentication
    response = self.client.get(reverse('shop_order_lines', kwargs={"id":1}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # fetch shop order lines with authentication but invalid data
    response = self.client.post(reverse("token_obtain_pair"), \
               {"email":self.shop.email, "password":"test@123"}, \
               format="json")
    token = response.data["access"]
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')
    response = self.client.get(reverse('shop_order_lines', kwargs={"id":15}))
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_complete_an_order(self):
    # complete an order without authentication
    response = self.client.put(reverse('shop_order_complete', \
               kwargs={"id":self.ech.HORD}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # complete shop order with authentication but invalid data
    response = self.client.post(reverse("token_obtain_pair"), \
               {"email":self.shop.email, "password":"test@123"}, \
               format="json")
    token = response.data["access"]
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')
    response = self.client.put(reverse('shop_order_complete', \
               kwargs={"id":50}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # complete shop order with authentication and valid data
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')
    response = self.client.put(reverse('shop_order_complete', \
               kwargs={"id":self.ech.HORD}))
    self.assertEqual(response.status_code, status.HTTP_200_OK)   
    self.assertEqual(ECH.objects.get(HORD=self.ech.HORD).HSTS, \
                     "COMPLETED")

  def test_cancel_an_order(self):
    # complete an order without authentication
    response = self.client.put(reverse('shop_order_cancel', \
               kwargs={"id":self.ech.HORD}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # complete shop order with authentication but invalid data
    response = self.client.post(reverse("token_obtain_pair"), \
               {"email":self.shop.email, "password":"test@123"}, \
               format="json")
    token = response.data["access"]
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')
    response = self.client.put(reverse('shop_order_cancel', \
               kwargs={"id":50}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # complete shop order with authentication and valid data
    response = self.client.put(reverse('shop_order_cancel', \
               kwargs={"id":self.ech.HORD}))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(ECH.objects.get(HORD=self.ech.HORD).HSTS, \
                     "CANCELLED")
    

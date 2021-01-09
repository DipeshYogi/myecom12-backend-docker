from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .factories.shopkeeper import UserFactory, CategoryFactory, \
                                  ShopProfileFactory, ShopItemsFactory


class TestShopKeeperApp(TestCase):
  """
  Test Shopkeeperapp Views
  """

  def setUp(self):
    self.client = APIClient()
    self.user = UserFactory()
    self.category = CategoryFactory()

    # login user
    response = self.client.post(reverse('token_obtain_pair'), \
               {"email":self.user.email, "password":"test@123"}, \
               format="json")
    self.token = response.data["access"]

  def test_shop_profile_creation(self):
    # test shop profile creation without authentication
    shop_profile = {
      "shop_name": "My Shop",
      "category": self.category.cat_name
    }

    response = self.client.post(reverse("create_shop_profile"), \
                shop_profile, format="json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test shop profile creation
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    response = self.client.post(reverse("create_shop_profile"), \
               shop_profile, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # check data
    self.assertEqual(response.data["shop_name"], shop_profile["shop_name"])
    self.assertEqual(response.data["category"], shop_profile["category"])
    self.assertEqual(response.data["is_verified"], False)
    self.assertEqual(response.data["free_delivery"], False)
    self.assertEqual(response.data["baggit_support"], False)

  def test_get_shop_profile(self):
    profile = ShopProfileFactory(shopid=self.user, category=self.category)

    # test unauthorized shop profile fetch
    response = self.client.get(reverse("shop_details"), format="json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test authorized shop profile fetch
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.token}')
    response = self.client.get(reverse("shop_details"), format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test response data
    self.assertEqual(response.data['ShopInfo']['shopid'], profile.shopid_id)
    self.assertEqual(response.data['ShopInfo']['shop_name'], profile.shop_name)
    self.assertEqual(response.data['ShopInfo']['category'], profile.category.cat_name)
  
  def test_update_shop_profile(self):
    profile = ShopProfileFactory(shopid=self.user, category=self.category)
    category2 = CategoryFactory(cat_name='Footwear')

    # test unauthorized shop profile update
    response = self.client.put(reverse("shop_details"), format="json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test authorized shop profile fetch with invalid data
    upd_profile = {
      "shop_name": 1,
      "category": "Invalid"
    }
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.token}')
    response = self.client.put(reverse("shop_details"), upd_profile, \
                               format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test authorized shop profile fetch with valid data
    upd_profile = {
      "shop_name": 1,
      "category": category2.cat_name
    }
    self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.token}')
    response = self.client.put(reverse("shop_details"), upd_profile, \
                               format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test updated data
    self.assertEqual(response.data["category"], category2.cat_name)

  def test_item_creation(self):
    data = {
      "item_name": "test item",
      "list_price": 20
    }
    inv_data = {
      "list_price": "price"
    }

    # test unauthorized item creation
    response = self.client.post(reverse("add_items"), data, format="json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test authorized item creation with invalid data
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    response = self.client.post(reverse("add_items"), inv_data, format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test authorized item creation with valid data
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    response = self.client.post(reverse("add_items"), data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)   

    # test created data
    self.assertEqual(response.data['itemInfo']['item_name'], data['item_name'])

  def test_get_items_by_shop(self):
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    # get items with no data available
    response = self.client.get(reverse("get_items_by_shop"))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # insert items and get the same
    profile = ShopProfileFactory(shopid=self.user, category=self.category)
    item = ShopItemsFactory(shopid = self.user)
    response = self.client.get(reverse("get_items_by_shop"))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertContains(response, item.item_name)
    self.assertContains(response, item.shopid.id)
    self.assertContains(response, item.list_price)

  
  def test_get_items_by_shopid(self):
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    # get items with no data available
    response = self.client.get(reverse("get_items_by_shop_id", \
                               kwargs={"shopid":self.user.id}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # insert items and get the same
    profile = ShopProfileFactory(shopid=self.user, category=self.category)
    item = ShopItemsFactory(shopid = self.user)
    response = self.client.get(reverse("get_items_by_shop_id", \
                            kwargs={"shopid":self.user.id}))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertContains(response, item.item_name)
    self.assertContains(response, item.shopid.id)
    self.assertContains(response, item.list_price)

  def test_item_update(self):
    upd_data = {
      "item_name":"New item"
    }
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    # update items with no data available
    response = self.client.put(reverse("update_items", \
                               kwargs={"id":1}), upd_data)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   

    # insert items and get the same
    profile = ShopProfileFactory(shopid=self.user, category=self.category)
    item = ShopItemsFactory(shopid = self.user)
    self.assertEqual(item.item_name, 'test item')
    response = self.client.put(reverse("update_items", \
                               kwargs={"id":item.id}), upd_data)
    self.assertContains(response, upd_data['item_name'])


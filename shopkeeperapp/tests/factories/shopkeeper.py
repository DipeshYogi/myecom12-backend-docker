import factory
from django.contrib.auth import get_user_model
from shopkeeperapp.models import Category, ShopProfile, \
                                 ShopItems


class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()

  email = factory.Sequence(lambda n: "test{}@gmail.com".format(n))
  password = factory.PostGenerationMethodCall('set_password', 'test@123')
  name = "test1"
  phone = "9786273621"
  date_of_birth = "1994-10-11"
  user_type = "CUSTOMER"


class CategoryFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Category
  
  cat_name = "Grocery"
  desc = "Grocery"


class ShopProfileFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ShopProfile
  
  shopid = factory.SubFactory(UserFactory)
  shop_name = "My Shop"
  category = factory.SubFactory(CategoryFactory)


class ShopItemsFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ShopItems
  
  shopid = factory.SubFactory(UserFactory)
  item_name = "test item"
  list_price = 10

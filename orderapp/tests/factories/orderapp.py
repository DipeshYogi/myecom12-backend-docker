import factory
from django.contrib.auth import get_user_model
from orderapp.models import ECH, ECL


class CustomerFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()
  
  email = factory.Sequence(lambda n: f'test{n}@gmail.com')
  password = factory.PostGenerationMethodCall('set_password', 'test@123')
  name = "test1"
  phone = "9786273621"
  date_of_birth = "1994-10-11"
  user_type = "CUSTOMER"


class ShopkeeperFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()
  
  email = factory.Sequence(lambda n: f'test_shop{n}@gmail.com')
  password = factory.PostGenerationMethodCall('set_password', 'test@123')
  name = "test1"
  phone = "9786273621"
  date_of_birth = "1994-10-11"
  user_type = "SHOPKEEPER"


class ECHFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ECH
  
  HORD = factory.Sequence(lambda n: n+1)
  HCUST = factory.SubFactory(CustomerFactory)
  HSHOP = factory.SubFactory(ShopkeeperFactory)
  HSTS = "ONGOING"
  HSNME = "Test Shop"
  HEDTE = "2020-12-02"


class ECLFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ECL
  
  LORD = factory.SubFactory(ECHFactory)
  LLINE = factory.Sequence(lambda n:n+1)
  LPROD = factory.Sequence(lambda n: f"Item{n}")
  LQORD = 1
  LPRIC = 20
  LDISC = 0
import factory 
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()
  
  email = factory.Sequence(lambda n: f"test{n}@gmail.com")
  password = factory.PostGenerationMethodCall('set_password', 'test@123')
  name = "test1"
  phone = "9786273621"
  date_of_birth = "1994-10-11"
  user_type = "CUSTOMER"
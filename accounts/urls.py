from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ModTokenObtainPairView

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('update/<int:id>/', views.UpdateUserView.as_view(), \
                             name='updated_user_profile' ),

    path('token/', ModTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
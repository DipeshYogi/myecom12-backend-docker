from django.urls import path
from . import views

urlpatterns = [
    path('shop-profile/', views.ShopProfileList.as_view(), \
                          name="create_shop_profile"),
    path('shop-profile-detail/', views.ShopProfileDetail.as_view(), \
                                 name="shop_details"),
    path('shop-profile/items/', views.GetItemsByShop.as_view(), \
                                name="get_items_by_shop"),
    path('shop-profile/shop-items/<int:shopid>/', views.GetItemsByShopId.as_view(), \
                                                  name="get_items_by_shop_id"),
    path('shop-profile/items/add/', views.AddItemsByShop.as_view(), \
                                    name="add_items"),
    path('shop-profile/items/update/<int:id>/', \
          views.UpdateItemByShop.as_view(), name="update_items"),
    path('categories/', views.GetCategoryInfo.as_view()),
    path('categories/add/', views.AddCategory.as_view()),
    path('categories/edit/<str:cat>/', views.EditCategory.as_view()),
    path('categories/shops/', views.GetShopsByCategory.as_view()),
    path('top-deals/', views.GetTopDeals.as_view()),
    path('top-shops/', views.GetTopShops.as_view())
]
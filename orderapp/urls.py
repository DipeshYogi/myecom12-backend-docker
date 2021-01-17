from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateOrder.as_view()),
    path('my-orders/', views.GetUserOrders.as_view()),
    path('shop-orders/', views.GetShopOrderHeader.as_view(), name="shop_order"),
    path('shop-order-lines/<int:id>/', views.GetShopOrderLines.as_view(), \
         name="shop_order_lines"),
    path('shop-order-complete/<int:id>/', views.CompleteOrder.as_view(), \
         name="shop_order_complete"), 
    path('shop-order-cancel/<int:id>/', views.CancelOrder.as_view(), \
         name="shop_order_cancel"),
]
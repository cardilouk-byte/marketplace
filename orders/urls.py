from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add'),
    path('update/<int:item_id>/', views.update_item, name='update'),
    path('remove/<int:item_id>/', views.remove_item, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),
]

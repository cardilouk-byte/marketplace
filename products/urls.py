from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('boutique/', views.product_list, name='list'),
    path('produit/<slug:slug>/', views.product_detail, name='detail'),
    path('categories/', views.product_list, name='categories'),
    path('categorie/<slug:slug>/', views.category_view, name='category'),
]

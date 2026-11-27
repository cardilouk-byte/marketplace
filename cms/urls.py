from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]

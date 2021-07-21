from django.urls import path
from .views import index, products

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', products, name='category'),
]

from django.urls import path
from adminapp.views import (
    users,
    user_create,
    user_update,
    product_update,
    user_delete,
    category_create,
    categories,
    category_delete,
    category_update,
    products,
    product_read,
    product_create,
    product_delete,
    UserListView,
    UserCreateView,
    ProductDetailView,
    ProductCategoryCreateView,
    ProductCategoryUpdateView,
    ProductCategoryDeleteView,
    ProductCategoryListView
)

app_name = 'adminapp'

urlpatterns = [
   # рабочий path('users/create/', user_create, name='user_create'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    # рабочий path('users/read/', users, name='users'),
    path('users/read/', UserListView.as_view(), name='users'),
    path('users/read/page/<int:page>/', users, name='users_page'),
    path('users/update/<int:pk>/', user_update, name='user_update'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),

    # рабочий path('categories/create/', category_create, name='category_create'),
    path('categories/create/', ProductCategoryCreateView.as_view(), name='category_create'),
    # рабочий path('categories/read/', categories, name='categories'),
    path('categories/read/', ProductCategoryListView.as_view(), name='categories'),
    path('categories/read/page/<int:page>/', categories, name='categories_page'),
    # path('categories/update/<int:pk>/', category_update, name='category_update'),
    path('categories/update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='category_update'),
    # path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
    path('categories/delete/<int:pk>/', ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', product_create, name='product_create'),
    path('products/read/category/<int:pk>/', products, name='products'),
    path('products/read/category/<int:pk>/page/<int:page>/', products, name='products_page'),
    # рабочий path('products/read/<int:pk>/', product_read, name='product_read'),
    path('products/read/<int:pk>/', ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
]

import random
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_links_menu_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
    return text['links_menu']  # возвратили массив ссылок


def get_category_list():
    links_menu = []
    for elem in ProductCategory.objects.all():
        links_menu.append({'href': f'{elem.pk}/', 'name': elem.name})
    return links_menu


def get_same_products(hot_product):
    same_products = Product.objects.filter(is_active=True).select_related('category').exclude(pk=hot_product.pk)[:3]
    return same_products


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    products = Product.objects.all().order_by('price')

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True).order_by('price')
            category = {'pk': 0, 'name': 'все'}

        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)


        context = {
            'title': title,
            'links_menu': links_menu,
            'same_products': same_products,
            'category': category,
            'related_products': same_products,
            'products': products_paginator,
            'hot_product': hot_product,
        }
        return render(request, 'mainapp/products.html', context)

    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
    }
    return render(request, 'mainapp/products.html', context)



def product(request, pk):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    product1 = get_object_or_404(Product, pk=pk)

    same_products = get_same_products(product)
    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)
    
# Вариант со словарем, файлом, заглушкой из БД. Оставлено для бэкапа.
def index(request):
    title = 'каталог'

    links_menu = [
        {'href': 'index', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    context = {
        'title': title,
        'links_menu': links_menu,
    }

    products = Product.objects.all()[:7]

    context2 = {
        'title': title,
        'links_menu': get_links_menu_from_file('mainapp/products.json'),
        'related_products': products,
    }

    context3 = {
        'title': title,
        'links_menu': get_category_list(),
        'related_products': products,
    }

    return render(request, 'mainapp/products.html', context3)

import random
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse




def get_links_menu_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
    return text['links_menu']  # возвратили массив ссылок


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter()

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)





def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).order_by('price')



def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True).order_by('price')


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)

def get_category_list():
    links_menu = []
    for elem in ProductCategory.objects.all():
        links_menu.append({'href': f'{elem.pk}/', 'name': elem.name})
    return links_menu


def get_same_products(hot_product):
    same_products = Product.objects.filter(is_active=True).select_related('category').exclude(pk=hot_product.pk)[:3]
    return same_products


def get_hot_product():
    products = get_products()

    return random.sample(list(products), 1)[0]


def products(request, pk=None, page=1):
    title = 'продукты'

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    links_menu = get_links_menu()
    products = get_products_orederd_by_price()

    if pk is not None:
        if pk == 0:
            products = products
            category = {'pk': 0, 'name': 'все'}
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

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
            'hot_product': hot_product,
            'same_products': same_products,
            'products': products_paginator,
            'category': category,
        }
        return render(request=request, template_name='mainapp/products.html', context=context)


    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
    }

    return render(request=request, template_name='mainapp/products.html', context=context)



def products_ajax(request, pk=None, page=1):
   if request.is_ajax():
       links_menu = get_links_menu()

       if pk:
           if pk == '0':
               category = {
                   'pk': 0,
                   'name': 'все'
               }
               products = get_products_orederd_by_price()
           else:
               category = get_category(pk)
               products = get_products_in_category_orederd_by_price(pk)

           paginator = Paginator(products, 2)
           try:
               products_paginator = paginator.page(page)
           except PageNotAnInteger:
               products_paginator = paginator.page(1)
           except EmptyPage:
               products_paginator = paginator.page(paginator.num_pages)

           content = {
               'links_menu': links_menu,
               'category': category,
               'products': products_paginator,
           }

           result = render_to_string(
                        'mainapp/includes/inc_products_list_content.html',
                        context=content,
                        request=request)

           return JsonResponse({'result': result})




def product(request, pk):
    title = 'продукты'
    links_menu = get_links_menu()

    product = get_product(pk)

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

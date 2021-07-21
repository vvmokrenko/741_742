from django.shortcuts import render
import json

from mainapp.models import Product, ProductCategory


def get_links_menu_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
    return text['links_menu']  # возвратили массив ссылок


def get_category_list():
    links_menu = []
    for elem in ProductCategory.objects.all():
        links_menu.append({'href': f'{elem.pk}/', 'name': elem.name})
    return links_menu


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

def products(request, pk=None):
    # Заглушка. Здесь д.б. обработка товаров по переданной категории.
    print(f'pk={pk}')
    return render(request)
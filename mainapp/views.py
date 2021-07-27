from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
import json

def get_links_menu_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
    return text['links_menu']  # возвратили массив ссылок


def get_category_list():
    links_menu = []
    for elem in ProductCategory.objects.all():
        links_menu.append({'href': f'{elem.pk}/', 'name': elem.name})
    return links_menu

def products(request, pk=None):
    title = 'продукты'

    links_menu = ProductCategory.objects.all()
    same_products = Product.objects.all()[:4]

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'related_products': same_products,
            'products': products,
            'basket': basket,
        }
        return render(request, 'mainapp/products.html', context)

    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'products': products,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context)
    
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

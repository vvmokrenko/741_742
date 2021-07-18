from django.shortcuts import render
import json

def get_links_menu_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
    return text['links_menu'] # возвратили массив ссылок



def index(request):
    title = 'кателог'

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

    context2 =  {
        'title': title,
        'links_menu': get_links_menu_from_file('mainapp/products.json'),
    }
    return render(request, 'mainapp/products.html', context2)

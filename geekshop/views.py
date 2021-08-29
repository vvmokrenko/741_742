from django.shortcuts import render


def index(request):
    title = 'Магазин'

    context = {
        'title': title,
        'slogan': 'супер предложения',
    }

    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'КОНтакты'

    address_list = [
        {'city': 'Москва', 'phone': '+7-495-888-8888', 'email': 'info@geekshop.ru', 'address': 'В пределах МКАД'},
        {'city': 'Санкт-Петербург', 'phone': '+7-812-888-8888', 'email': 'info@geekshop.spb.ru', 'address': 'В пределах КАД'},
        {'city': 'Краснодар', 'phone': '+7-861-888-8888', 'email': 'info@geekshop.krd.ru', 'address': 'Уточнить по телефону'},
    ]

    context = {
        'title': title,
        'address_list': address_list,
    }

    return render(request, 'geekshop/contact.html', context)

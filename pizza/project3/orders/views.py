# from django.http import HttpResponse
# from django.shortcuts import render

# Create your views here.
# def index(request):
#   return HttpResponse('Project 3: TODO')


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.models import User

from texts.models import Language
from texts.models import to_dict_list

from quantities.models import Currency

from .models import Setting
from .models import UserSetting

from .models import Dish
from .models import Order, OrderDish, OrderType
from .models import OrderFlavor, OrderSize
from .models import get_order
from .models import get_order_dish

from django.http import JsonResponse

import stripe


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('menu'))


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        return render(request, 'orders/login.html', {'message': None})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(
            request, 'orders/login.html',
            {'message': 'Invalid credentials.'}
        )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        return render(
            request, 'orders/register.html',
            {'message': None}
        )

    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.filter(username=username)
    if len(user) < 1:
        user = User.objects.create_user(username=username, password=password)
        if user is None:
            return render(
                request, 'orders/register.html',
                {'message': 'Invalid credentials.'}
            )
    else:
        user = user[0]
        user.is_active = True
        user.set_password(password)
        user.save()

    login(request, user)

    return HttpResponseRedirect(reverse('index'))


def unregister_view(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'orders/unregister.html')

    if request.POST['confirm-cancel'] == 'confirm':
        request.user.is_active = False
        request.user.save()
        logout(request)

    return HttpResponseRedirect(reverse('index'))


def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    user_settings = UserSetting.get_first(user=request.user)
    language = None
    currency = None
    user_settings_dict = {}
    if user_settings:
        if user_settings.language:
            language = user_settings.language

        if user_settings.currency:
            currency = user_settings.currency

        user_settings.to_dict(user_settings_dict, language=language)

    settings = Setting.objects.first()
    settings_dict = {}
    if settings:
        settings.to_dict(settings_dict, language=language)

    languages_dict_list = to_dict_list(
        Language.objects, 'code__sort_number'
    )
    currencies_dict_list = to_dict_list(
        Currency.objects, 'code__sort_number', language=language
    )
    dishes_dict_list = to_dict_list(
        Dish.objects, 'sort_number', language=language, currency=currency
    )

    put_columns_to_dishes(dishes_dict_list)

    context = {
        'settings': settings_dict,
        'user_settings': user_settings_dict,
        'languages': languages_dict_list,
        'currencies': currencies_dict_list,
        'dishes': dishes_dict_list,
    }

    request.session['page'] = reverse('menu')

    return render(request, 'orders/menu.html', context)


def select_language(request, language_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    language = Language.objects.filter(id=language_id).first()

    user_settings = UserSetting.objects.filter(user=request.user).first()
    if not user_settings:
        user_settings = UserSetting(user=request.user, language=language)
    else:
        user_settings.language = language

    user_settings.save()

    return HttpResponseRedirect(request.session['page'])


def select_currency(request, currency_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    currency = Currency.objects.filter(id=currency_id).first()

    user_settings = UserSetting.objects.filter(user=request.user).first()
    if not user_settings:
        user_settings = UserSetting(user=request.user, currency=currency)
    else:
        user_settings.currency = currency

    user_settings.save()

    return HttpResponseRedirect(request.session['page'])


def put_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        dish_id = request.POST["dish-id"]
        type_id = request.POST["type-id"]
        flavor_id = request.POST["flavor-id"]
        size_id = request.POST["size-id"]

        dish_id = None if dish_id == 'None' else dish_id
        type_id = None if type_id == 'None' else type_id
        flavor_id = None if flavor_id == 'None' else flavor_id
        size_id = None if size_id == 'None' else size_id

        return HttpResponseRedirect(reverse(
                'order_item',
                args=[dish_id, type_id, flavor_id, size_id]
            )
        )

    else:
        return HttpResponseRedirect(reverse("index"))


def alter_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        order_dish_id = request.POST["order-dish-id"]
        order_type_id = request.POST["order-type-id"]
        order_flavor_id = request.POST["order-flavor-id"]
        order_size_id = request.POST["order-size-id"]

        order_dish_id = None if order_dish_id == 'None' else order_dish_id
        order_type_id = None if order_type_id == 'None' else order_type_id
        order_flavor_id = (
            None if order_flavor_id == 'None' else order_flavor_id
        )
        order_size_id = None if order_size_id == 'None' else order_size_id

        order_dish = OrderDish.objects.filter(id=order_dish_id).first()
        order_type = OrderType.objects.filter(id=order_type_id).first()
        order_flavor = OrderFlavor.objects.filter(id=order_flavor_id).first()
        order_size = OrderSize.objects.filter(id=order_size_id).first()

        if request.POST["submit"] == 'inc-dish-count':
            order_dish.count += 1
            order_dish.save()
        elif request.POST["submit"] == 'dec-dish-count':
            if order_dish.count > 0:
                order_dish.count -= 1
                order_dish.save()

        elif request.POST["submit"] == 'inc-type-count':
            order_type.count += 1
            order_type.save()
        elif request.POST["submit"] == 'dec-type-count':
            if order_type.count > 0:
                order_type.count -= 1
                order_type.save()

        elif request.POST["submit"] == 'inc-flavor-count':
            order_flavor.count += 1
            order_flavor.save()
        elif request.POST["submit"] == 'dec-flavor-count':
            if order_flavor.count > 0:
                order_flavor.count -= 1
                order_flavor.save()

        elif request.POST["submit"] == 'inc-size-count':
            order_size.count += 1
            order_size.save()
        elif request.POST["submit"] == 'dec-size-count':
            if order_size.count > 0:
                order_size.count -= 1
                order_size.save()

        dish_id = None if not order_dish else order_dish.menu.id
        type_id = None if not order_type else order_type.menu.id
        flavor_id = None if not order_flavor else order_flavor.menu.id
        size_id = None if not order_size else order_size.menu.id

        return HttpResponseRedirect(reverse(
                'order_item',
                args=[dish_id, type_id, flavor_id, size_id]
            )
        )

    else:
        return HttpResponseRedirect(reverse("index"))


def order_item(request, dish_id, type_id, flavor_id, size_id):
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return HttpResponse(f'{dish_id}/{type_id}/{flavor_id}/{size_id}')
    """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method != "GET":
        return HttpResponseRedirect(reverse('index'))

    dish_id = None if dish_id == 'None' else dish_id
    type_id = None if type_id == 'None' else type_id
    flavor_id = None if flavor_id == 'None' else flavor_id
    size_id = None if size_id == 'None' else size_id

    user_settings = UserSetting.get_first(user=request.user)
    language = None
    currency = None
    user_settings_dict = {}
    if user_settings:
        if user_settings.language:
            language = user_settings.language

        if user_settings.currency:
            currency = user_settings.currency

        user_settings.to_dict(user_settings_dict, language=language)

    settings = Setting.objects.first()
    settings_dict = {}
    if settings:
        settings.to_dict(settings_dict, language=language)

    languages_dict_list = to_dict_list(
        Language.objects, 'code__sort_number'
    )
    currencies_dict_list = to_dict_list(
        Currency.objects, 'code__sort_number', language=language
    )

    order = get_order(user=request.user)

    order_dish = get_order_dish(order, dish_id, type_id, flavor_id, size_id)

    order_dish_dict = {}
    order_dish.to_dict(order_dish_dict, language=language, currency=currency)

    calc_order_dish_price(order_dish_dict)

    put_columns_to_order_dish(order_dish_dict)

    context = {
        'settings': settings_dict,
        'user_settings': user_settings_dict,
        'languages': languages_dict_list,
        'currencies': currencies_dict_list,
        'order_dish': order_dish_dict,
    }

    request.session['page'] = reverse(
        'order_item',
        args=[dish_id, type_id, flavor_id, size_id]
    )

    return render(request, 'orders/order-item.html', context)


def cart(request):
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return HttpResponse(f'Shopping Cart')
    """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    user_settings = UserSetting.get_first(user=request.user)
    language = None
    currency = None
    user_settings_dict = {}
    if user_settings:
        if user_settings.language:
            language = user_settings.language

        if user_settings.currency:
            currency = user_settings.currency

        user_settings.to_dict(user_settings_dict, language=language)

    settings = Setting.objects.first()
    settings_dict = {}
    if settings:
        settings.to_dict(settings_dict, language=language)

    languages_dict_list = to_dict_list(
        Language.objects, 'code__sort_number'
    )
    currencies_dict_list = to_dict_list(
        Currency.objects, 'code__sort_number', language=language
    )

    order = get_order(user=request.user)

    order_dict = {}
    order.to_dict(order_dict, language=language, currency=currency)

    calc_order_price(order_dict)

#    put_columns_to_order_dishes(order_dishes_dict_list)

    context = {
        'settings': settings_dict,
        'user_settings': user_settings_dict,
        'languages': languages_dict_list,
        'currencies': currencies_dict_list,
        'order': order_dict,
    }

    request.session['page'] = reverse('cart')

    return render(request, 'orders/cart.html', context)


def clear_cart(request):
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return HttpResponse(f'Shopping Cart')
    """

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    order = Order.objects.filter(user=request.user).first()
    if order:
        order.cancel()

    return HttpResponseRedirect(reverse('cart'))


def calc_order_price(order):
    value = 0
    unit = None

    for order_dish in order['dishes']:
        p = calc_order_dish_price(order_dish)
        value += p['value']
        unit = p['unit']

    price = {
        'value': value,
        'unit': unit,
    }

    order['price'] = price

    return price


def calc_order_dish_price(order_dish):
    value = 0
    unit = None

    for order_type in order_dish['types']:
        p = calc_order_type_price(order_type)
        value += p['value']
        unit = p['unit']

    for order_flavor in order_dish['flavors']:
        p = calc_order_flavor_price(order_flavor)
        value += p['value']
        unit = p['unit']

    for order_adding in order_dish['addings']:
        p = calc_order_adding_price(order_adding)
        value += p['value']
        unit = p['unit']

    for order_size in order_dish['sizes']:
        p = calc_order_size_price(order_size)
        value += p['value']
        unit = p['unit']

    if order_dish['plain']:
        value += (
            order_dish['count'] *
            order_dish['menu']['trait']['quantity']['converted']['value']
        )
        unit = order_dish['menu']['trait']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
    }

    order_dish['price'] = price

    return price


def calc_order_type_price(order_type):
    value = 0
    unit = None

    for order_flavor in order_type['flavors']:
        p = calc_order_flavor_price(order_flavor)
        value += p['value']
        unit = p['unit']

    for order_adding in order_type['addings']:
        p = calc_order_adding_price(order_adding)
        value += p['value']
        unit = p['unit']

    for order_size in order_type['sizes']:
        p = calc_order_size_price(order_size)
        value += p['value']
        unit = p['unit']

    if order_type['plain']:
        value += (
            order_type['count'] *
            order_type['menu']['trait']['quantity']['converted']['value']
        )
        unit = order_type['menu']['trait']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
    }

    order_type['price'] = price

    return price


def calc_order_flavor_price(order_flavor):
    value = 0
    unit = None

    for order_adding in order_flavor['addings']:
        p = calc_order_adding_price(order_adding)
        value += p['value']
        unit = p['unit']

    for order_size in order_flavor['sizes']:
        p = calc_order_size_price(order_size)
        value += p['value']
        unit = p['unit']

    if order_flavor['plain']:
        value += (
            order_flavor['count'] *
            order_flavor['menu']['trait']['quantity']['converted']['value']
        )
        unit = order_flavor['menu']['trait']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
    }

    order_flavor['price'] = price

    return price


def calc_order_adding_price(order_adding):
    value = 0
    unit = None

    for order_flavor in order_adding['flavors']:
        p = calc_order_flavor_price(order_flavor)
        value += p['value']
        unit = p['unit']

    for order_size in order_adding['sizes']:
        p = calc_order_size_price(order_size)
        value += p['value']
        unit = p['unit']

    if order_adding['plain']:
        value += (
            order_adding['count'] *
            order_adding['menu']['trait']['quantity']['converted']['value']
        )
        unit = order_adding['menu']['trait']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
    }

    order_adding['price'] = price

    return price


def calc_order_size_price(order_size):
    value = (
        order_size['count'] *
        order_size['menu']['trait']['quantity']['converted']['value']
    )
    unit = order_size['menu']['trait']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    order_size['price'] = price

    return price


def get_pages_basic_data(
        request, language, currency,
        settings_dict, user_settings_dict
        ):

    user_settings = UserSetting.get_first(user=request.user)
    if user_settings:
        if user_settings.language:
            language = user_settings.language

        if user_settings.currency:
            currency = currency
            currency = user_settings.currency

        user_settings.to_dict(user_settings_dict, language=language)

    settings = Setting.objects.first()
    if settings:
        settings.to_dict(settings_dict, language=language)


def success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    language = None
    currency = None
    settings_dict = {}
    user_settings_dict = {}
    get_pages_basic_data(
        request, language, currency,
        settings_dict, user_settings_dict
    )

    languages_dict_list = to_dict_list(
        Language.objects, 'code__sort_number'
    )

    currencies_dict_list = to_dict_list(
        Currency.objects, 'code__sort_number', language=language
    )

    context = {
        'settings': settings_dict,
        'user_settings': user_settings_dict,
        'languages': languages_dict_list,
        'currencies': currencies_dict_list,
    }

    request.session['page'] = reverse('success')

    return render(request, 'orders/success.html', context)


def cancel(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    language = None
    currency = None
    settings_dict = {}
    user_settings_dict = {}
    get_pages_basic_data(
        request, language, currency,
        settings_dict, user_settings_dict
    )

    languages_dict_list = to_dict_list(
        Language.objects, 'code__sort_number'
    )

    currencies_dict_list = to_dict_list(
        Currency.objects, 'code__sort_number', language=language
    )

    context = {
        'settings': settings_dict,
        'user_settings': user_settings_dict,
        'languages': languages_dict_list,
        'currencies': currencies_dict_list,
    }

    request.session['page'] = reverse('cancel')

    return render(request, 'orders/cancel.html', context)


# This is a sample test API key.
# Sign in to see examples pre-filled with your key.
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


YOUR_DOMAIN = 'http://localhost:4242'


def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        # 'unit_amount': 2000,
                        'unit_amount': int(float(request.read()) * 100),
                        'product_data': {
                            'name': 'Stubborn Attachments',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse(error=str(e))


def put_columns_to_dishes(dishes):
    for dish in dishes:
        types_columns = {}
        put_types(types_columns, dish)
        dish['types_columns'] = types_columns

        flavors_columns = {}
        put_flavors(flavors_columns, dish)
        dish['flavors_columns'] = flavors_columns

        addings_columns = {}
        put_addings(addings_columns, dish)
        dish['addings_columns'] = addings_columns


def put_columns_to_order_dish(order_dish):
    types_columns = {}
    put_order_types(types_columns, order_dish)
    order_dish['types_columns'] = types_columns

    flavors_columns = {}
    put_order_flavors(flavors_columns, order_dish)
    order_dish['flavors_columns'] = flavors_columns

    addings_columns = {}
    put_order_addings(addings_columns, order_dish)
    order_dish['addings_columns'] = addings_columns


def put_types(columns, table):
    sizes = []
    for type in table['types']:
        flavors_columns = {}
        put_flavors(flavors_columns, type)
        type['flavors_columns'] = flavors_columns

        addings_columns = {}
        put_addings(addings_columns, type)
        type['addings_columns'] = addings_columns

        put_sizes(sizes, type)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    columns['sizes'] = sizes


def put_order_types(columns, order_table):
    sizes = []
    for type in order_table['types']:
        flavors_columns = {}
        put_order_flavors(flavors_columns, type)
        type['flavors_columns'] = flavors_columns

        addings_columns = {}
        put_order_addings(addings_columns, type)
        type['addings_columns'] = addings_columns

        put_order_sizes(sizes, type)

    sizes.sort(key=lambda size: size['menu']['sort_number'], reverse=False)
    columns['sizes'] = sizes


def put_flavors(columns, table):
    sizes = []
    for flavor in table['flavors']:
        addings_columns = {}
        put_addings(addings_columns, flavor)
        flavor['addings_columns'] = addings_columns

        put_sizes(sizes, flavor)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    columns['sizes'] = sizes


def put_order_flavors(columns, order_table):
    sizes = []
    for flavor in order_table['flavors']:
        addings_columns = {}
        put_order_addings(addings_columns, flavor)
        flavor['addings_columns'] = addings_columns

        put_order_sizes(sizes, flavor)

    sizes.sort(key=lambda size: size['menu']['sort_number'], reverse=False)
    columns['sizes'] = sizes


def put_addings(columns, table):
    sizes = []
    for adding in table['addings']:
        flavors_columns = {}
        put_flavors(flavors_columns, adding)
        adding['flavors_columns'] = flavors_columns

        put_sizes(sizes, adding)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    columns['sizes'] = sizes


def put_order_addings(columns, order_table):
    sizes = []
    for adding in order_table['addings']:
        flavors_columns = {}
        put_order_flavors(flavors_columns, adding)
        adding['flavors_columns'] = flavors_columns

        put_order_sizes(sizes, adding)

    sizes.sort(key=lambda size: size['menu']['sort_number'], reverse=False)
    columns['sizes'] = sizes


def put_sizes(columns, table):
    for size in table['sizes']:
        inserted = False
        for column in columns:
            if column['trait']['short_name'] == size['trait']['short_name']:
                inserted = True
                break

        if not inserted:
            columns.append(size)


def put_order_sizes(columns, order_table):
    for size in order_table['sizes']:
        inserted = False
        for column in columns:
            column_short_name = column['menu']['trait']['short_name']
            size_short_name = size['menu']['trait']['short_name']
            if column_short_name == size_short_name:
                inserted = True
                break

        if not inserted:
            columns.append(size)

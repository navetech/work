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
from texts.models import to_dict, to_dict_list

from quantities.models import Currency

from .models import Setting
from .models import UserSetting

from .models import Menu

from .models import menu_item_to_dict

#from .models import Order, OrderDish, OrderType
#from .models import OrderFlavor, OrderAdding, OrderSize

from .models import create_order_dish, get_order_dishes

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


def get_pages_basic_data(request):
    user_settings = UserSetting.get_first(user=request.user)
    if user_settings:
        if user_settings.language:
            language = user_settings.language
        else:
            language = None

        if user_settings.currency:
            currency = user_settings.currency
        else:
            currency = None

        user_settings_dict = to_dict(user_settings, language=language)
    else:
        language = None
        currency = None
        user_settings_dict = {}

    settings = Setting.objects.first()
    if settings:
        settings_dict = to_dict(settings, language=language)
    else:
        settings_dict = {}

    languages = to_dict_list(
        Language.objects, 'code__sort_number'
    )
    currencies = to_dict_list(
        Currency.objects, 'code__sort_number', language=language
    )

    pages_basic_data = {}
    pages_basic_data['language'] = language
    pages_basic_data['currency'] = currency
    pages_basic_data['user_settings'] = user_settings_dict
    pages_basic_data['settings'] = settings_dict
    pages_basic_data['languages'] = languages
    pages_basic_data['currencies'] = currencies

    return pages_basic_data


def insert_item_sizes(sizes_list, item):
    for item_size in item['sizes']:
        inserted = False
        for list_size in sizes_list:
            if list_size['name'] == item_size['name']:
                inserted = True
                break

        if not inserted:
            sizes_list.append(item_size)


def build_flavors_table(item):
    table = {}

    sizes = []
    for flavor in item['flavors']:
        insert_item_sizes(sizes, item=flavor)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    table['sizes'] = sizes

    return table


def build_item_sizes_columns(sizes, item):
    columns = []
    for size in sizes:
        present = False
        for item_size in item['sizes']:
            if size['name'] == item_size['name']:
                present = True
                break

        if present:
            columns.append(item_size)
        else:
            columns.append(None)

    return columns


def fill_menu_item_tables(item):
    menu_item = item

    if 'dishes' in item and item['dishes']:
        list = []
        for dish in item['dishes']:
            elem = fill_menu_item_tables(dish)
            list.append(elem)
        menu_item['dishes'] = list

    if 'types' in item and item['types']:
        list = []
        for type in item['types']:
            elem = fill_menu_item_tables(type)
            list.append(elem)
        menu_item['types'] = list

    if 'flavors' in item and item['flavors']:
        flavors_table = build_flavors_table(item)
        menu_item['flavors_table'] = flavors_table

        for flavor in item['flavors']:
            flavor['size_columns'] = build_item_sizes_columns(
                sizes=flavors_table['sizes'], item=flavor
            )

    if 'sizes' in item and item['sizes']:
        menu_item['sizes'] = item['sizes']

    if 'addinga' in item and item['adding']:
        menu_item['adding'] = item['adding']

    return menu_item


def build_menu(**settings):
    menu_object = MenuItem.objects.filter(container=None).first()
    container_dict = {}
    menu = menu_item_to_dict(container_dict, menu_object, **settings)

    menu = fill_menu_item_tables(menu)

    return menu


def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    pages_basic_data = get_pages_basic_data(request)

    language = pages_basic_data['language']
    currency = pages_basic_data['currency']
    user_settings = pages_basic_data['user_settings']
    settings = pages_basic_data['settings']
    languages = pages_basic_data['languages']
    currencies = pages_basic_data['currencies']

    menu = build_menu(language=language, currency=currency)

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
        'menu': menu,
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

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        dish_id = request.POST["dish-id"]
        type_id = request.POST["type-id"]
        flavor_id = request.POST["flavor-id"]
        size_id = request.POST["size-id"]

        dish_id = None if dish_id == 'None' else dish_id
        type_id = None if type_id == 'None' else type_id
        flavor_id = None if flavor_id == 'None' else flavor_id
        size_id = None if size_id == 'None' else size_id

        user = request.user
        order = Order.objects.filter(user=user).first()
        if not order:
            order = Order(user=user)
            order.save()

            order_dish = create_order_dish(order, dish_id, type_id, flavor_id, size_id)
            if not order_dish:
                order.cancel()
        else:
            order_dishes = get_order_dishes(order, dish_id, type_id, flavor_id, size_id)
            if len(order_dishes) > 0:
                order_dish = order_dishes[0]
            else:
                order_dish = create_order_dish(order, dish_id, type_id, flavor_id, size_id)

        return HttpResponseRedirect(reverse(
                'order_item', args=[order_dish.id]
            )
        )


def alter_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        order_dish_id = request.POST["order-dish-id"]
        order_type_id = request.POST["order-type-id"]
        order_flavor_id = request.POST["order-flavor-id"]
        order_size_id = request.POST["order-size-id"]

        post_keys = request.POST.keys()

        if "order-adding-id" in post_keys:
            order_adding_id = request.POST["order-adding-id"]
        else:
            order_adding_id = None

        if "order-adding-size-id" in post_keys:
            order_adding_size_id = request.POST["order-adding-size-id"]
        else:
            order_adding_size_id = None

        if "order-adding-flavor-id" in post_keys:
            order_adding_flavor_id = request.POST["order-adding-flavor-id"]
        else:
            order_adding_flavor_id = None

        if "order-adding-flavor-size-id" in post_keys:
            order_adding_flavor_size_id = request.POST["order-adding-flavor-size-id"]
        else:
            order_adding_flavor_size_id = None

        order_dish_id = None if order_dish_id == 'None' else order_dish_id
        order_type_id = None if order_type_id == 'None' else order_type_id
        order_flavor_id = (
            None if order_flavor_id == 'None' else order_flavor_id
        )
        order_size_id = None if order_size_id == 'None' else order_size_id
        order_adding_id = (
            None if order_adding_id == 'None' else order_adding_id
        )
        order_adding_size_id = (
            None if order_adding_size_id == 'None' else order_adding_size_id
        )
        order_adding_flavor_id = (
            None if order_adding_flavor_id == 'None' else order_adding_flavor_id
        )
        order_adding_flavor_size_id = (
            None if order_adding_flavor_size_id == 'None' else order_adding_flavor_size_id
        )

        order_dish = OrderDish.objects.filter(id=order_dish_id).first()
        order_type = OrderType.objects.filter(id=order_type_id).first()
        order_flavor = OrderFlavor.objects.filter(id=order_flavor_id).first()
        order_size = OrderSize.objects.filter(id=order_size_id).first()

        order_adding = OrderAdding.objects.filter(id=order_adding_id).first()
        order_adding_size = OrderSize.objects.filter(id=order_adding_size_id).first()
        order_adding_flavor = OrderFlavor.objects.filter(id=order_adding_flavor_id).first()
        order_adding_flavor_size = OrderSize.objects.filter(id=order_adding_flavor_size_id).first()

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

        elif request.POST["submit"] == 'inc-adding-count':
            order_adding.count += 1
            order_adding.save()
        elif request.POST["submit"] == 'dec-adding-count':
            if order_adding.count > 0:
                order_adding.count -= 1
                order_adding.save()

        elif request.POST["submit"] == 'inc-adding-size-count':
            order_adding_size.count += 1
            order_adding_size.save()
        elif request.POST["submit"] == 'dec-adding-size-count':
            if order_adding_size.count > 0:
                order_adding_size.count -= 1
                order_adding_size.save()

        elif request.POST["submit"] == 'inc-adding-flavor-count':
            order_adding_flavor.count += 1
            order_adding_flavor.save()
        elif request.POST["submit"] == 'dec-adding-flavor-count':
            if order_adding_flavor.count > 0:
                order_adding_flavor.count -= 1
                order_adding_flavor.save()

        elif request.POST["submit"] == 'inc-adding-flavor-size-count':
            order_adding_flavor_size.count += 1
            order_adding_flavor_size.save()
        elif request.POST["submit"] == 'dec-adding-flavor-size-count':
            if order_adding_flavor_size.count > 0:
                order_adding_flavor_size.count -= 1
                order_adding_flavor_size.save()

        check = order_dish.check_count()
        if check['count'] > 0:
            return HttpResponseRedirect(reverse(
                    'order_item', args=[order_dish.id]
                )
            )
        else:
            order_dish.cancel()
            return HttpResponseRedirect(reverse('cart'))


def order_item(request, order_dish_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method != "GET":
        return HttpResponseRedirect(reverse('index'))

    order_dish = OrderDish.objects.filter(id=order_dish_id).first()
    if not order_dish:
        return HttpResponseRedirect(reverse('cart'))

    check = order_dish.check_count()
    if check['count'] < 1:
        order_dish.cancel()
        return HttpResponseRedirect(reverse('cart'))

    pages_basic_data = get_pages_basic_data(request)

    language = pages_basic_data['language']
    currency = pages_basic_data['currency']
    user_settings = pages_basic_data['user_settings']
    settings = pages_basic_data['settings']
    languages = pages_basic_data['languages']
    currencies = pages_basic_data['currencies']

    order_dish_dict = to_dict(order_dish, language=language, currency=currency)

    calc_order_dish_price(order_dish_dict)

    put_columns_to_order_dish(order_dish_dict)

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
        'order_dish': order_dish_dict,
    }

    request.session['page'] = reverse(
        'order_item', args=[order_dish.id]
    )

    return render(request, 'orders/order-item.html', context)


def cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    pages_basic_data = get_pages_basic_data(request)

    language = pages_basic_data['language']
    currency = pages_basic_data['currency']
    user_settings = pages_basic_data['user_settings']
    settings = pages_basic_data['settings']
    languages = pages_basic_data['languages']
    currencies = pages_basic_data['currencies']

    order = Order.objects.filter(user=request.user).first()
    if order:
        order_check = order.check_count()
        if order_check['count'] > 0:
            order_dict = to_dict(order, language=language, currency=currency)
            calc_order_price(order_dict)
        else:
            order.cancel()
            order_dict = {}
            order_check = {}
    else:
        order_dict = {}
        order_check = {}

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
        'order': order_dict,
        'order_check': order_check,
    }

    request.session['page'] = reverse('cart')

    return render(request, 'orders/cart.html', context)


def clear_cart(request):
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


def calc_plain_order_object_price(order_object):
    if order_object['plain']:
        if 'quantity' in order_object['menu'].keys():
            if 'converted' in order_object['menu']['quantity']:
                value = (
                    order_object['count'] *
                    order_object['menu']['quantity']['converted']['value']
                )
                unit = order_object['menu']['quantity']['converted']['unit']

                price = {
                    'value': value,
                    'unit': unit,
                }

                return price

    return None


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

    p = calc_plain_order_object_price(order_dish)
    if p:
        value += p['value']
        unit = p['unit']

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

    p = calc_plain_order_object_price(order_type)
    if p:
        value += p['value']
        unit = p['unit']

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

    p = calc_plain_order_object_price(order_flavor)
    if p:
        value += p['value']
        unit = p['unit']

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

    p = calc_plain_order_object_price(order_adding)
    if p:
        value += p['value']
        unit = p['unit']

    price = {
        'value': value,
        'unit': unit,
    }

    order_adding['price'] = price

    return price


def calc_order_size_price(order_size):
    value = (
        order_size['count'] *
        order_size['menu']['quantity']['converted']['value']
    )
    unit = order_size['menu']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    order_size['price'] = price

    return price


def success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    pages_basic_data = get_pages_basic_data(request)

    user_settings = pages_basic_data['user_settings']
    settings = pages_basic_data['settings']
    languages = pages_basic_data['languages']
    currencies = pages_basic_data['currencies']

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
    }

    request.session['page'] = reverse('success')

    return render(request, 'orders/success.html', context)


def cancel(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    pages_basic_data = get_pages_basic_data(request)

    user_settings = pages_basic_data['user_settings']
    settings = pages_basic_data['settings']
    languages = pages_basic_data['languages']
    currencies = pages_basic_data['currencies']

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
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


def put_order_flavors(columns, order_table):
    sizes = []
    for flavor in order_table['flavors']:
        addings_columns = {}
        put_order_addings(addings_columns, flavor)
        flavor['addings_columns'] = addings_columns

        put_order_sizes(sizes, flavor)

    sizes.sort(key=lambda size: size['menu']['sort_number'], reverse=False)
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


def put_order_sizes(columns, order_table):
    for size in order_table['sizes']:
        inserted = False
        for column in columns:
            column_short_name = column['menu']['short_name']
            size_short_name = size['menu']['short_name']
            if column_short_name == size_short_name:
                inserted = True
                break

        if not inserted:
            columns.append(size)

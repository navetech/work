from django.http import HttpResponse
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

from .models import menu_elem_to_dict

from .models import get_order_item_by_user, create_order_item_for_user

from .models import Order, OrderItem
"""
from .models import OrderMenu, OrderDish, OrderType
from .models import OrderFlavor, OrderSize
from .models import OrderAdding, OrderAddingFlavor
"""

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


def insert_menu_elem_sizes(sizes, elem):
    for elem_size in elem['sizes']:
        inserted = False
        for size in sizes:
            if size['name'] == elem_size['name']:
                inserted = True
                break

        if not inserted:
            sizes.append(elem_size)

    return sizes


def build_menu_elem_flavors_table(elem):
    table = {}

    sizes = []
    for flavor in elem['flavors']:
        sizes = insert_menu_elem_sizes(sizes, flavor)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    table['sizes'] = sizes

    return table


def build_menu_elem_sizes_columns(sizes, elem):
    columns = []
    for size in sizes:
        present = False
        for elem_size in elem['sizes']:
            if size['name'] == elem_size['name']:
                present = True
                break

        if present:
            columns.append(elem_size)
        else:
            columns.append(None)

    return columns


def fill_menu_elem_tables(elem):
    if 'dishes' in elem and elem['dishes']:
        lista = []
        for dish in elem['dishes']:
            e = fill_menu_elem_tables(dish)
            lista.append(e)
        elem['dishes'] = lista

    if 'types' in elem and elem['types']:
        lista = []
        for type in elem['types']:
            e = fill_menu_elem_tables(type)
            lista.append(e)
        elem['types'] = lista

    if 'flavors' in elem and elem['flavors']:
        flavors_table = build_menu_elem_flavors_table(elem)
        elem['flavors_table'] = flavors_table

        for flavor in elem['flavors']:
            flavor['size_columns'] = build_menu_elem_sizes_columns(
                sizes=flavors_table['sizes'], elem=flavor
            )

    return elem


def add_elem_globals(globals, elem):
    if 'globals' in elem and elem['globals']:
        for elem_global in elem['globals']:
            if elem_global not in globals:
                globals.append(elem_global)

    return globals


def add_sub_globals(globals, elem):
    if 'dishes' in elem and elem['dishes']:
        for dish in elem['dishes']:
            globals = add_elem_globals(globals, dish)

    if 'types' in elem and elem['types']:
        for type in elem['types']:
            globals = add_elem_globals(globals, type)

    if 'flavors' in elem and elem['flavors']:
        for flavor in elem['flavors']:
            globals = add_elem_globals(globals, flavor)

    return globals


def build_globals(elem):
    globals = []

    if 'addings' in elem and elem['addings']:
        for adding in elem['addings']:
            if 'flavors_set' in adding and adding['flavors_set']:
                if adding['flavors_set'] not in globals:
                    globals.append(adding['flavors_set'])

    globals = add_sub_globals(globals, elem)

    globals.sort(
        key=lambda flavors_set: flavors_set['sort_number'],
        reverse=False
    )

    return globals


def prune_elem_globals(elem, container_globals):
    if 'globals' in elem and elem['globals']:

        if 'addings' in elem and elem['addings']:
            for adding in elem['addings']:
                if 'flavors_set' in adding and adding['flavors_set']:
                    if adding['flavors_set'] in elem['globals']:
                        elem['globals'].remove(adding['flavors_set'])

        if container_globals:
            for container_global in container_globals:
                if container_global in elem['globals']:
                    elem['globals'].remove(container_global)

        elem['globals'].sort(
            key=lambda flavors_set: flavors_set['sort_number'],
            reverse=False
        )

    return elem


def prune_sub_globals(elem):
    if 'globals' in elem:
        container_globals = elem['globals']
    else:
        container_globals = None

    if 'dishes' in elem and elem['dishes']:
        for dish in elem['dishes']:
            dish = prune_elem_globals(dish, container_globals)

    if 'types' in elem and elem['types']:
        for type in elem['types']:
            type = prune_elem_globals(type, container_globals)

    if 'flavors' in elem and elem['flavors']:
        for flavor in elem['flavors']:
            flavor = prune_elem_globals(flavor, container_globals)

    return elem


def fill_globals(elem):
    if 'dishes' in elem and elem['dishes']:
        for dish in elem['dishes']:
            dish = fill_globals(dish)

    if 'types' in elem and elem['types']:
        for type in elem['types']:
            type = fill_globals(type)

    if 'flavors' in elem and elem['flavors']:
        for flavor in elem['flavors']:
            flavor = fill_globals(flavor)

    globals = build_globals(elem)
    if globals:
        elem['globals'] = globals

    elem = prune_sub_globals(elem)

    return elem


def fill_sub_globals(elem):
    if 'dishes' in elem and elem['dishes']:
        for dish in elem['dishes']:
            dish = fill_globals(dish)

    if 'types' in elem and elem['types']:
        for type in elem['types']:
            type = fill_globals(type)

    if 'flavors' in elem and elem['flavors']:
        for flavor in elem['flavors']:
            flavor = fill_globals(flavor)

    elem = prune_sub_globals(elem)

    return elem


def build_menu(**settings):
    menu_object = Menu.objects.first()
    container_dict = {}
    menu = menu_elem_to_dict(container_dict, menu_object, **settings)

    menu = fill_menu_elem_tables(menu)

    menu = fill_sub_globals(menu)

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
    print('//////////////////////')
    print('put_order')
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        menu_id = request.POST["menu-id"]
        dish_id = request.POST["dish-id"]
        type_id = request.POST["type-id"]
        flavor_id = request.POST["flavor-id"]
        size_id = request.POST["size-id"]

        menu_id = None if menu_id == 'None' else menu_id
        dish_id = None if dish_id == 'None' else dish_id
        type_id = None if type_id == 'None' else type_id
        flavor_id = None if flavor_id == 'None' else flavor_id
        size_id = None if size_id == 'None' else size_id

        print('put_order 2')
        print('//////////////////////')
        user = request.user
        order_status = 'InCart'

        order_item = get_order_item_by_user(
            menu_id, dish_id, type_id,
            flavor_id, size_id,
            user, order_status
        )
        print('output get_order_item_by_user')
        print(order_item)
        print('-------------------------------')
        if not order_item:
            order_item = create_order_item_for_user(
                menu_id, dish_id, type_id,
                flavor_id, size_id,
                user, order_status
            )

        if order_item:
            order_item_id = order_item.id
        else:
            order_item_id = 'None'

        return HttpResponseRedirect(reverse(
                'order_item', args=[order_item_id]
            )
        )


def alter_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        order_item_id = request.POST["order-item-id"]

        """
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

        order_item_id = None if order_item_id == 'None' else order_item_id

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
        """

        order_item = OrderItem.objects.filter(id=order_item_id).first()

        """
        order_adding = OrderAdding.objects.filter(id=order_adding_id).first()
        order_adding_size = OrderSize.objects.filter(id=order_adding_size_id).first()
        order_adding_flavor = OrderFlavor.objects.filter(id=order_adding_flavor_id).first()
        order_adding_flavor_size = OrderSize.objects.filter(id=order_adding_flavor_size_id).first()
        """

        if request.POST["submit"] == 'inc-order-item-count':
            order_item.count += 1
            order_item.save()
        elif request.POST["submit"] == 'dec-order-item-count':
            order_item.count -= 1
            order_item.save()

        """
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
        """

        return HttpResponseRedirect(reverse(
            'order_item', args=[order_item.id]
            )
        )


def calc_order_size_price(order_size):
    value = order_size['elem']['quantity']['converted']['value']
    unit = order_size['elem']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    return price


def calc_order_elem_price(order_elem):
    value = order_elem['elem']['quantity']['converted']['value']
    unit = order_elem['elem']['quantity']['converted']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    return price
    

def calc_order_item_price(order_item):
    value = 0
    unit = None

    price = {
        'value': value,
        'unit': unit,
        }

    if order_item['size']:
        price = calc_order_size_price(order_item['size'])
    elif order_item['flavor']:
        price = calc_order_elem_price(order_item['flavor'])
    elif order_item['type']:
        price = calc_order_elem_price(order_item['type'])
    elif order_item['dish']:
        price = calc_order_elem_price(order_item['dish'])
    elif order_item['menu']:
        price = calc_order_elem_price(order_item['menu'])

    price['value'] *= order_item['count']

    return price


def fill_order_item_price(order_item):
    price = calc_order_item_price(order_item)
    order_item['price'] = price

    return order_item


def order_item(request, order_item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method != "GET":
        return HttpResponseRedirect(reverse('index'))

    order_item_id = None if order_item_id == 'None' else order_item_id

    if order_item_id is None:
        return HttpResponseRedirect(reverse('index'))

    order_item_object = OrderItem.objects.filter(id=order_item_id).first()
    if not order_item_object:
        return HttpResponseRedirect(reverse('cart'))

    if order_item_object.count < 1:
        order_item_object.cancel()
        return HttpResponseRedirect(reverse('cart'))

    pages_basic_data = get_pages_basic_data(request)

    language = pages_basic_data['language']
    currency = pages_basic_data['currency']
    user_settings = pages_basic_data['user_settings']
    settings = pages_basic_data['settings']
    languages = pages_basic_data['languages']
    currencies = pages_basic_data['currencies']

    order_item = to_dict(order_item_object, language=language, currency=currency)
    order_item = fill_order_item_price(order_item)

    """"
    order_item_dict = calc_order_item_price(order_item_dict)
    order_item = fill_order_item_prices(order_item)

    order_item_dict = put_columns_to_order_item(order_item_dict)
    order_item = fill_order_item_tables(order_item)

    menu = menu_elem_to_dict(container_dict, menu_object, **settings)

    menu = fill_menu_elem_tables(menu)

    menu = fill_sub_globals(menu)
    """

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
        'order_item': order_item,
    }

    request.session['page'] = reverse(
        'order_item', args=[order_item_id]
    )

    return render(request, 'orders/order-item.html', context)


def fill_order_price(order):
    value = 0
    unit = None

    price = {
        'value': value,
        'unit': unit,
        }

    for order_item in order['items']:
        order_item = fill_order_item_price(order_item)

        price['value'] += order_item['price']['value']
        price['unit'] = order_item['price']['unit']

    order['price'] = price

    return order


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

    user = request.user
    status='InCart'
    order_object = Order.objects.filter(user=user, status=status).first()
    if not order_object:
        order = {}
    elif order_object.items.count() < 1:
        order_object.cancel()
        order = {}
    else:
            order = to_dict(order_object, language=language, currency=currency)
            order = fill_order_price(order)

    context = {
        'settings': settings,
        'user_settings': user_settings,
        'languages': languages,
        'currencies': currencies,
        'order': order,
    }

    request.session['page'] = reverse('cart')

    return render(request, 'orders/cart.html', context)


def clear_cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    status='InCart'
    orders = Order.objects.filter(user=user, status=status).all()
    for order in orders:
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


def success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    status='InCart'
    orders = Order.objects.filter(user=user, status=status).all()
    for order in orders:
        order.cancel()

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

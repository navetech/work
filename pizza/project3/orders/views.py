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

from .models import Dish
from .models import Order, OrderDish, OrderType
from .models import OrderFlavor, OrderAdding, OrderSize

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

    dishes = to_dict_list(
        Dish.objects, 'sort_number', language=language, currency=currency
    )

    menu = {}
    menu['dishes'] = dishes

    menu = fill_menu_item(menu)

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


def fill_menu_item(item):
    if not item:
        return item
    
    item = fill_is_plain(item)

    if not 'has_children' in item or not item['has_children']:
        return item
    
    elems = 'dishes'
    item = fill_menu_item_from_elems(item, elems)

    elems = 'types'
    item = fill_menu_item_from_elems(item, elems)

    elems = 'flavors'
    item = fill_menu_item_from_elems(item, elems)

    elems = 'addings'
    item = fill_menu_item_from_elems(item, elems)

    elems = 'sizes'
    item = fill_menu_item_from_elems(item, elems)

    if 'table' in item and item['table']:
        item['table'] = fill_table(item['table'])

    return item


def fill_is_plain(item):
    if item:
        has_children = True
        is_plain = False

        if not 'dishes' in item or not item['dishes']:
            if not 'types' in item or not item['types']:
                if not 'flavors' in item or not item['flavors']:
                    if not 'addings' in item or not item['addings']:
                        if not 'sizes' in item or not item['sizes']:
                            has_children = False

                            if 'quantity' in item and item['quantity']:
                                is_plain = True

        item['has_children'] = has_children
        item['is_plain'] = is_plain

    return item


def fill_menu_item_from_elems(item, elems):
    if item and elems:
        if elems in item:
            plain_elems = []
            table_elems = []
            full_elems = []

            item[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

            for elem in item[elems]:
                elem = fill_menu_item(elem)

                if elem:
                    if 'is_plain' in elem and elem['is_plain']:
                        plain_elems.append(elem)
                    else:
                        if 'plain' in elem and elem['plain']:
                            table_elems.append(elem)

                        full_elems.append(elem)

            if len(plain_elems) > 0 and len(plain_elems) >= len(item[elems]):
                if not 'plain' in item:
                    item['plain'] = {}
                if not elems in item['plain']:
                    item['plain'][elems]= []
                item['plain'][elems].extend(plain_elems)

            if len(table_elems) > 0:
                if not 'table' in item:
                    item['table'] = {}
                if not elems in item['table']:
                    item['table'][elems] = []
                item['table'][elems].extend(table_elems)

            if len(full_elems) > 0:
                if not 'full' in item:
                    item['full'] = {}
                if not elems in item['full']:
                    item['full'][elems] = []
                item['full'][elems].extend(full_elems)

    return item


def fill_table(table):
    if table:
        table['headers'] = build_table_headers(table)

        table['lines'] = build_table_lines(table, table['headers'])

    return table


def build_table_headers(table):
    if not table:
        return None
        
    headers = {}

    elems = 'dishes'
    headers = fill_headers_from_elems(headers, table, elems)

    elems = 'types'
    headers = fill_headers_from_elems(headers, table, elems)

    elems = 'flavors'
    headers = fill_headers_from_elems(headers, table, elems)

    elems = 'addings'
    headers = fill_headers_from_elems(headers, table, elems)

    elems = 'sizes'
    headers = fill_headers_from_elems(headers, table, elems)
    
    return headers


def fill_headers_from_elems(headers, table, elems):
    if table and elems:
        if elems in table:
            table[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

            for elem in table[elems]:
                headers = fill_headers_from_elem(headers, elem)

    return headers


def fill_headers_from_elem(headers, elem):
    if elem:
        if 'plain' in elem:
            struct = elem['plain']

            struct_elems = 'dishes'
            headers = fill_headers_from_struct_elems(headers, struct, struct_elems)

            struct_elems = 'types'
            headers = fill_headers_from_struct_elems(headers, struct, struct_elems)

            struct_elems = 'flavors'
            headers = fill_headers_from_struct_elems(headers, struct, struct_elems)

            struct_elems = 'addings'
            headers = fill_headers_from_struct_elems(headers, struct, struct_elems)

            struct_elems = 'sizes'
            headers = fill_headers_from_struct_elems(headers, struct, struct_elems)

    return headers


def fill_headers_from_struct_elems(headers, struct, elems):
    if struct and elems:
        if elems in struct:
            if struct[elems]:
                struct[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

                if not elems in headers:
                    headers[elems] = []

                for elem in struct[elems]:
                    if not elem in headers[elems]:
                        headers[elems].append(elem)

                headers[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

    return headers


def build_table_lines(table, headers):
    if not (table and headers):
        return None

    lines = {}

    elems = 'dishes'
    lines[elems] = build_table_lines_from_elems(table, headers, elems)

    elems = 'types'
    lines[elems] = build_table_lines_from_elems(table, headers, elems)

    elems = 'flavors'
    lines[elems] = build_table_lines_from_elems(table, headers, elems)

    elems = 'addings'
    lines[elems] = build_table_lines_from_elems(table, headers, elems)

    elems = 'sizes'
    lines[elems] = build_table_lines_from_elems(table, headers, elems)

    return lines


def build_table_lines_from_elems(table, headers, elems):
    if not (table and headers and elems):
        return None

    if not elems in table:
        return None

    table[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

    elems_lines = []

    for elem in table[elems]:
        line = build_line_from_elem(headers, elem)

        elems_lines.append(line)

    return elems_lines


def build_line_from_elem(headers, elem):
    if not (headers and elem):
        return None

    if not 'plain' in elem:
        return None

    columns = {}

    struct = elem['plain']

    struct_elems = 'dishes'
    columns[struct_elems]= build_columns_from_struct_elems(headers, struct, struct_elems)

    struct_elems = 'types'
    columns[struct_elems]= build_columns_from_struct_elems(headers, struct, struct_elems)

    struct_elems = 'flavors'
    columns[struct_elems]= build_columns_from_struct_elems(headers, struct, struct_elems)

    struct_elems = 'addings'
    columns[struct_elems]= build_columns_from_struct_elems(headers, struct, struct_elems)

    struct_elems = 'sizes'
    columns[struct_elems]= build_columns_from_struct_elems(headers, struct, struct_elems)

    elem['columns'] = columns

    return elem


def build_columns_from_struct_elems(headers, struct, elems):
    if not (headers and struct and elems):
        return None

    if not elems in headers:
        return None

    headers[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

    if elems in struct:
        struct[elems].sort(key=lambda elem: elem['sort_number'], reverse=False)

    elems_columns = []
    for h_elem in headers[elems]:
        column = None
        if elems in struct:
            for s_elem in struct[elems]:
                if h_elem == s_elem:
                    column = s_elem
                    break

        elems_columns.append(column)

    return elems_columns


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


def build_object_columns(object):
    columns = []
    column = {}

    if 'dishes' in object:
        list= []
        for obj in object['dishes']:
            cols = build_object_columns(obj)
            if not cols:
                list.append(obj)
        if list:
            list.sort(key=lambda elem: elem['sort_number'], reverse=False)
            column['dish'] = list
            columns.append(column['dish'])

    if 'types' in object:
        list= []
        for obj in object['types']:
            cols = build_object_columns(obj)
            if not cols:
                list.append(obj)
        if list:
            list.sort(key=lambda elem: elem['sort_number'], reverse=False)
            column['type'] = list
            columns.append(column['type'])

    if 'flavors' in object:
        list= []
        for obj in object['flavors']:
            cols = build_object_columns(obj)
            if not cols:
                list.append(obj)
        if list:
            list.sort(key=lambda elem: elem['sort_number'], reverse=False)
            column['flavor'] = list
            columns.append(column['flavor'])

    if 'addings' in object:
        list= []
        for obj in object['addings']:
            cols = build_object_columns(obj)
            if not cols:
                list.append(obj)
        if list:
            list.sort(key=lambda elem: elem['sort_number'], reverse=False)
            column['adding'] = list
            columns.append(column['adding'])

    if 'sizes' in object:
        list= []
        for obj in object['sizes']:
            cols = build_object_columns(obj)
            if not cols:
                list.append(obj)
        if list:
            list.sort(key=lambda elem: elem['sort_number'], reverse=False)
            column['size'] = list
            columns.append(column['size'])

    return columns


def build_objects_columns(objects):
    sizes = []

    for object in objects:
        if 'types' in object:
            object['types_columns'] = build_objects_columns(object['types'])

        if 'flavors' in object:
            object['flavors_columns'] = build_objects_columns(object['flavors'])

        if 'addings' in object:
            object['addings_columns'] = build_objects_columns(object['addings'])

        if 'sizes' in object:
            object['sizes_columns'] = build_objects_columns(object['sizes'])

        put_sizes_columns(sizes, dish)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)

    for dish in dishes:
        dish['size_columns'] = put_sizes_columns(sizes, dish)

    return dishes


def build_dishes_columns(dishes):
    sizes = []

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

        put_sizes(sizes, dish)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)

    for dish in dishes:
        dish['size_columns'] = put_sizes_columns(sizes, dish)

    return dishes


def put_columns_to_dishes(dishes):
    sizes = []

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

        put_sizes(sizes, dish)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)

    for dish in dishes:
        dish['size_columns'] = put_sizes_columns(sizes, dish)

    return dishes


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

    for flavor in table['flavors']:
        flavor['size_columns'] = put_sizes_columns(sizes, flavor)


def put_sizes_columns(inserted_sizes, table):
    columns = []
    for s in inserted_sizes:
        present = False
        for size in table['sizes']:
            if s['short_name'] == size['short_name']:
                present = True
                break

        if present:
            columns.append(size)
        else:
            columns.append(None)

    return columns


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
            if column['short_name'] == size['short_name']:
                inserted = True
                break

        if not inserted:
            columns.append(size)


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

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

from .models import elem_to_dict
from .models import adjust_count_limit_dict, adjust_count_limit


from .models import get_order_item_by_user, create_order_item_for_user

from .models import Order, OrderItem
from .models import OrderAdding, OrderAddingFlavor, OrderAddingFlavorSize

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
    not_empty_columns_count = 0

    for size in sizes:
        present = False
        for elem_size in elem['sizes']:
            if size['name'] == elem_size['name']:
                present = True
                break

        if present:
            columns.append(elem_size)
            not_empty_columns_count += 1
        else:
            columns.append(None)

    if not_empty_columns_count < 1:
        columns = []

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
    menu = elem_to_dict(container_dict, menu_object, **settings)

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

        user = request.user
        order_status = 'InCart'

        order_item = get_order_item_by_user(
            menu_id, dish_id, type_id,
            flavor_id, size_id,
            user, order_status
        )

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


def get_adding_flavors_selection_limit(adding):
    limit = adding.flavors_selection_limit

    flavors_selection_limit = adjust_count_limit(limit)

    return flavors_selection_limit


def alter_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        post_keys = request.POST.keys()

        if "order-item-id" in post_keys:
            order_item_id = request.POST["order-item-id"]
        else:
            order_item_id = None

        if "order-adding-id" in post_keys:
            order_adding_id = request.POST["order-adding-id"]
        else:
            order_adding_id = None

        if "order-adding-flavor-id" in post_keys:
            order_adding_flavor_id = request.POST["order-adding-flavor-id"]
        else:
            order_adding_flavor_id = None

        if "order-adding-flavor-size-id" in post_keys:
            order_adding_flavor_size_id = (
                request.POST["order-adding-flavor-size-id"]
            )
        else:
            order_adding_flavor_size_id = None

        order_item_id = None if order_item_id == 'None' else order_item_id

        order_adding_id = (
            None if order_adding_id == 'None' else order_adding_id
        )
        order_adding_flavor_id = (
            None if order_adding_flavor_id ==
            'None' else order_adding_flavor_id
        )

        order_adding_flavor_size_id = (
            None if order_adding_flavor_size_id ==
            'None' else order_adding_flavor_size_id
        )

        order_item = OrderItem.objects.filter(id=order_item_id).first()
        order_adding = OrderAdding.objects.filter(id=order_adding_id).first()
        order_adding_flavor = OrderAddingFlavor.objects.filter(
            id=order_adding_flavor_id
        ).first()
        order_adding_flavor_size = OrderAddingFlavorSize.objects.filter(
            id=order_adding_flavor_size_id
        ).first()

        if request.POST["submit"] == 'inc-order-item-count':
            order_item.count += 1
            order_item.save()
        elif request.POST["submit"] == 'dec-order-item-count':
            order_item.count -= 1
            order_item.save()

        elif request.POST["submit"] == 'order-adding-flavor-select':
            limit = get_adding_flavors_selection_limit(order_adding.elem)

            if order_adding_flavor.selected:
                order_adding_flavor.selected = False
                order_adding_flavor.save()
                order_adding.flavors_selection_count -= 1
                order_adding.save()
            else:
                if (
                    limit['max'] < 0
                    or
                    order_adding.flavors_selection_count < limit['max']
                ):
                    order_adding_flavor.selected = True
                    order_adding_flavor.save()
                    order_adding.flavors_selection_count += 1
                    order_adding.save()

        elif request.POST["submit"] == 'order-adding-flavor-size-select':
            limit = get_adding_flavors_selection_limit(order_adding.elem)

            if order_adding_flavor_size.selected:
                order_adding_flavor_size.selected = False
                order_adding_flavor_size.save()
                order_adding_flavor.sizes_selection_count -= 1
                order_adding_flavor.save()

                if order_adding_flavor.sizes_selection_count < 1:
                    order_adding_flavor.selected = False
                    order_adding_flavor.save()

                order_adding.flavors_selection_count -= 1
                order_adding.save()
            else:
                for size in order_adding_flavor.sizes.all():
                    if size.selected:
                        size.selected = False
                        size.save()
                        order_adding_flavor.sizes_selection_count -= 1
                        order_adding_flavor.save()

                        if order_adding_flavor.sizes_selection_count < 1:
                            order_adding_flavor.selected = False
                            order_adding_flavor.save()

                        order_adding.flavors_selection_count -= 1
                        order_adding.save()

                if (
                    limit['max'] < 0
                    or
                    order_adding.flavors_selection_count < limit['max']
                ):
                    order_adding_flavor_size.selected = True
                    order_adding_flavor_size.save()
                    order_adding_flavor.sizes_selection_count += 1
                    order_adding_flavor.save()

                    order_adding_flavor.selected = True
                    order_adding_flavor.save()

                    order_adding.flavors_selection_count += 1
                    order_adding.save()

        return HttpResponseRedirect(reverse(
            'order_item', args=[order_item.id]
            )
        )


def fill_order_adding_flavor_size_price(
    order_adding_flavor_size, container_quantity
):
    value = 0

    unit = None
    if order_adding_flavor_size['elem']['quantity']:
        unit = (
            order_adding_flavor_size['elem']['quantity']['converted']['unit']
        )
    elif container_quantity:
        order_adding_flavor_size['elem']['quantity'] = container_quantity
        unit = (
            order_adding_flavor_size['elem']['quantity']['converted']['unit']
        )

    if (
        order_adding_flavor_size['selected'] and
        order_adding_flavor_size['elem']['quantity']
    ):
        value += (
            order_adding_flavor_size['elem']['quantity']['converted']['value']
        )
        unit = (
            order_adding_flavor_size['elem']['quantity']['converted']['unit']
        )

    price = {
        'value': value,
        'unit': unit,
        }

    order_adding_flavor_size['price'] = price

    return order_adding_flavor_size


def fill_order_adding_flavor_price(order_adding_flavor, container_quantity):
    value = 0

    unit = None
    if order_adding_flavor['elem']['quantity']:
        unit = order_adding_flavor['elem']['quantity']['converted']['unit']
    elif container_quantity:
        order_adding_flavor['elem']['quantity'] = container_quantity
        unit = order_adding_flavor['elem']['quantity']['converted']['unit']

    if (
        len(order_adding_flavor['sizes']) < 1 and
        order_adding_flavor['selected'] and
        order_adding_flavor['elem']['quantity']
    ):
        value += (
            order_adding_flavor['elem']['quantity']['converted']['value']
        )
        unit = (
            order_adding_flavor['elem']['quantity']['converted']['unit']
        )
    else:
        if order_adding_flavor['elem']['quantity']:
            container_quantity = order_adding_flavor['elem']['quantity']

        for order_adding_flavor_size in order_adding_flavor['sizes']:
            order_adding_flavor_size = fill_order_adding_flavor_size_price(
                order_adding_flavor_size, container_quantity
            )

            value += order_adding_flavor_size['price']['value']
            if order_adding_flavor_size['price']['unit']:
                unit = order_adding_flavor_size['price']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    order_adding_flavor['price'] = price

    return order_adding_flavor


def fill_order_adding_price(order_adding):
    value = 0

    unit = None
    if order_adding['elem']['quantity']:
        unit = order_adding['elem']['quantity']['converted']['unit']

    if len(order_adding['flavors']) < 1:
        if order_adding['elem']['quantity']:
            value += order_adding['elem']['quantity']['converted']['value']
            unit = order_adding['elem']['quantity']['converted']['unit']
    else:
        container_quantity = order_adding['elem']['quantity']

        for order_adding_flavor in order_adding['flavors']:
            order_adding_flavor = fill_order_adding_flavor_price(
                order_adding_flavor, container_quantity
            )

            value += order_adding_flavor['price']['value']
            if order_adding_flavor['price']['unit']:
                unit = order_adding_flavor['price']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    order_adding['price'] = price

    return order_adding


def fill_order_elem_price(order_elem):
    value = 0
    unit = None

    if order_elem['elem']['quantity']:
        value += order_elem['elem']['quantity']['converted']['value']
        unit = order_elem['elem']['quantity']['converted']['unit']

    for order_adding in order_elem['addings']:
        order_adding = fill_order_adding_price(order_adding)

        value += order_adding['price']['value']
        if order_adding['price']['unit']:
            unit = order_adding['price']['unit']

    price = {
        'value': value,
        'unit': unit,
        }

    order_elem['price'] = price

    return order_elem


def fill_order_item_price(order_item):
    value = 0
    unit = None

    price = {
        'value': value,
        'unit': unit,
        }

    if order_item['size']:
        order_elem = order_item['size']
        order_elem = fill_order_elem_price(order_elem)
        price = order_elem['price']
        order_item['size'] = order_elem

    elif order_item['flavor']:
        order_elem = order_item['flavor']
        order_elem = fill_order_elem_price(order_elem)
        price = order_elem['price']
        order_item['flavor'] = order_elem

    elif order_item['type']:
        order_elem = order_item['type']
        order_elem = fill_order_elem_price(order_elem)
        price = order_elem['price']
        order_item['type'] = order_elem

    elif order_item['dish']:
        order_elem = order_item['dish']
        order_elem = fill_order_elem_price(order_elem)
        price = order_elem['price']
        order_item['dish'] = order_elem

    elif order_item['menu']:
        order_elem = order_item['menu']
        order_elem = fill_order_elem_price(order_elem)
        price = order_elem['price']
        order_item['menu'] = order_elem

    price['value'] *= order_item['count']

    order_item['price'] = price

    return order_item


def fill_order_adding_status(order_adding):
    ready = True

    limit = order_adding['elem']['flavors_selection_limit']
    limit = adjust_count_limit_dict(limit)

    if order_adding['flavors_selection_count'] < limit['min']:
        selections_deficiency = True
    else:
        selections_deficiency = False

    if (
        limit['max'] >= 0 and
        order_adding['flavors_selection_count'] > limit['max']
    ):
        selections_excess = True
    else:
        selections_excess = False

    if selections_deficiency or selections_excess:
        ready = False

    status = {
        'ready': ready,
        'selections_deficiency': selections_deficiency,
        'selections_excess': selections_excess,
        }

    order_adding['status'] = status

    return order_adding


def fill_order_elem_status(order_elem):
    ready = True

    for order_adding in order_elem['addings']:
        order_adding = fill_order_adding_status(order_adding)

        if not order_adding['status']['ready']:
            ready = order_adding['status']['ready']

    status = {
        'ready': ready,
        }

    order_elem['status'] = status

    return order_elem


def fill_order_item_status(order_item):
    ready = True

    status = {
        'ready': ready,
        }

    if order_item['size']:
        order_elem = order_item['size']
        order_elem = fill_order_elem_status(order_elem)
        status = order_elem['status']
        order_item['size'] = order_elem

    elif order_item['flavor']:
        order_elem = order_item['flavor']
        order_elem = fill_order_elem_status(order_elem)
        status = order_elem['status']
        order_item['flavor'] = order_elem

    elif order_item['type']:
        order_elem = order_item['type']
        order_elem = fill_order_elem_status(order_elem)
        status = order_elem['status']
        order_item['type'] = order_elem

    elif order_item['dish']:
        order_elem = order_item['dish']
        order_elem = fill_order_elem_status(order_elem)
        status = order_elem['status']
        order_item['dish'] = order_elem

    elif order_item['menu']:
        order_elem = order_item['menu']
        order_elem = fill_order_elem_status(order_elem)
        status = order_elem['status']
        order_item['menu'] = order_elem

    order_item['status'] = status

    return order_item


def insert_order_adding_flavor_sizes(sizes, order_adding_flavor):
    for order_adding_flavor_size in order_adding_flavor['sizes']:
        inserted = False
        for size in sizes:
            if size['name'] == order_adding_flavor_size['elem']['name']:
                inserted = True
                break

        if not inserted:
            sizes.append(order_adding_flavor_size['elem'])

    return sizes


def insert_order_adding_flavor_special_sizes(sizes, order_adding_flavor):
    special_count = 0
    for order_adding_flavor_size in order_adding_flavor['sizes']:
        if order_adding_flavor_size['elem']['special']:
            special_count += 1
            inserted = False
            for size in sizes:
                if size['name'] == order_adding_flavor_size['elem']['name']:
                    inserted = True
                    break

            if not inserted:
                sizes.append(order_adding_flavor_size['elem'])

    if special_count < 1:
        for order_adding_flavor_size in order_adding_flavor['sizes']:
            if order_adding_flavor_size['selected']:
                inserted = False
                for size in sizes:
                    if (
                        size['name'] ==
                        order_adding_flavor_size['elem']['name']
                    ):
                        inserted = True
                        break

                if not inserted:
                    sizes.append(order_adding_flavor_size['elem'])

    return sizes


def build_order_adding_flavors_table(order_adding):
    table = {}

    sizes = []
    for order_adding_flavor in order_adding['flavors']:
        sizes = insert_order_adding_flavor_sizes(sizes, order_adding_flavor)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    table['sizes'] = sizes

    return table


def build_order_adding_special_flavors_table(order_adding):
    table = {}

    sizes = []
    for order_adding_flavor in order_adding['flavors']:
        if order_adding_flavor['elem']['special']:
            sizes = insert_order_adding_flavor_special_sizes(
                sizes, order_adding_flavor
            )

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
    table['sizes'] = sizes

    return table


def build_order_adding_flavor_sizes_columns(sizes, order_adding_flavor):
    columns = []
    not_empty_columns_count = 0

    for size in sizes:
        present = False
        for order_adding_flavor_size in order_adding_flavor['sizes']:
            if size['name'] == order_adding_flavor_size['elem']['name']:
                present = True
                break

        if present:
            columns.append(order_adding_flavor_size)
            not_empty_columns_count += 1
        else:
            columns.append(None)

    if not_empty_columns_count < 1:
        columns = []

    return columns


def fill_order_adding_tables(order_adding):
    if 'flavors' in order_adding and order_adding['flavors']:
        flavors_table = build_order_adding_flavors_table(order_adding)
        order_adding['flavors_table'] = flavors_table

        special_flavors_table = (
            build_order_adding_special_flavors_table(
                order_adding
            )
        )
        order_adding['special_flavors_table'] = special_flavors_table

        for order_adding_flavor in order_adding['flavors']:
            order_adding_flavor['size_columns'] = (
                build_order_adding_flavor_sizes_columns(
                    sizes=flavors_table['sizes'],
                    order_adding_flavor=order_adding_flavor
                )
            )

            if order_adding_flavor['elem']['special']:
                order_adding_flavor['special_size_columns'] = (
                    build_order_adding_flavor_sizes_columns(
                        sizes=special_flavors_table['sizes'],
                        order_adding_flavor=order_adding_flavor
                    )
                )


def fill_order_elem_tables(order_elem):
    for order_adding in order_elem['addings']:
        order_adding = fill_order_adding_tables(order_adding)

    return order_elem


def fill_order_item_tables(order_item):
    if 'flavor' in order_item and order_item['flavor']:
        order_elem = order_item['flavor']
        order_elem = fill_order_elem_tables(order_elem)
        order_item['flavor'] = order_elem

    elif 'type' in order_item and order_item['type']:
        order_elem = order_item['type']
        order_elem = fill_order_elem_tables(order_elem)
        order_item['type'] = order_elem

    elif 'dish' in order_item and order_item['dish']:
        order_elem = order_item['dish']
        order_elem = fill_order_elem_tables(order_elem)
        order_item['dish'] = order_elem

    elif 'menu' in order_item and order_item['menu']:
        order_elem = order_item['menu']
        order_elem = fill_order_elem_tables(order_elem)
        order_item['menu'] = order_elem

    return order_item


def fill_order_item(order_item):
    order_item = fill_order_item_tables(order_item)
    order_item = fill_order_item_status(order_item)
    order_item = fill_order_item_price(order_item)

    return order_item


def build_order_item(order_item_object, language, currency):
    if order_item_object:
        order_item = to_dict(
            order_item_object, language=language, currency=currency
        )
        if order_item:
            order_item = fill_order_item(order_item)
    else:
        order_item = {}

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

    order_item = build_order_item(
        order_item_object, language=language, currency=currency
    )

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
        price['value'] += order_item['price']['value']
        price['unit'] = order_item['price']['unit']

    order['price'] = price

    return order


def fill_order_status(order):
    ready = True

    for order_item in order['items']:
        if not order_item['status']['ready']:
            ready = order_item['status']['ready']

    status = {
        'ready': ready,
        }

    order['status'] = status

    return order


def fill_order(order):
    order = fill_order_price(order)
    order = fill_order_status(order)

    return order


def build_order(user, status, language, currency):
    order_object = Order.objects.filter(user=user, status=status).first()
    if not order_object:
        order = {}
    elif order_object.items.count() < 1:
        order_object.cancel()
        order = {}
    else:
        order = to_dict(order_object, language=language, currency=currency)
        for order_item in order['items']:
            order_item = fill_order_item(order_item)

        order = fill_order(order)

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
    status = 'InCart'
    order = build_order(user, status, language=language, currency=currency)

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
    status = 'InCart'
    orders = Order.objects.filter(user=user, status=status).all()
    for order in orders:
        order.cancel()

    return HttpResponseRedirect(reverse('cart'))


def success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    status = 'InCart'
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

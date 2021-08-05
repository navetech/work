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
from texts.models import to_dict_list

from quantities.models import Currency

from .models import Setting
from .models import UserSetting

from .models import Dish
from .models import get_order
from .models import get_order_dish


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

    return HttpResponseRedirect(reverse("index"))


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

    return HttpResponseRedirect(reverse("index"))


def order(request, dish_id, type_id, flavor_id, size_id):
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return HttpResponse(f'{dish_id}/{type_id}/{flavor_id}/{size_id}')
    """

    if not request.user.is_authenticated:
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

    context = {
        'settings': settings_dict,
        'user_settings': user_settings_dict,
        'languages': languages_dict_list,
        'currencies': currencies_dict_list,
        'order_dish': order_dish_dict,
    }

#    return HttpResponse(f'{dish_id}/{type_id}/{flavor_id}/{size_id}')

    return render(request, 'orders/order.html', context)


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


def put_flavors(columns, table):
    sizes = []
    for flavor in table['flavors']:
        addings_columns = {}
        put_addings(addings_columns, flavor)
        flavor['addings_columns'] = addings_columns

        put_sizes(sizes, flavor)

    sizes.sort(key=lambda size: size['sort_number'], reverse=False)
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


def put_sizes(columns, table):
    for size in table['sizes']:
        inserted = False
        for column in columns:
            if column['trait']['short_name'] == size['trait']['short_name']:
                inserted = True
                break

        if not inserted:
            columns.append(size)


"""
def get_order_dish(user, dish_id, type_id, flavor_id, size_id):
    pass
"""

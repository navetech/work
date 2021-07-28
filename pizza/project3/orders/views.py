from django.http import HttpResponse
#from django.shortcuts import render

# Create your views here.
#def index(request):
#    return HttpResponse("Project 3: TODO")


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.models import User

from django.core import serializers
import json


from .models import Dish
from .models import to_dict_list


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("menu"))


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        return render(request, "orders/login.html", {"message": None})
    
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        return render(request, "orders/register.html", {"message": None})

    username = request.POST["username"]
    password = request.POST["password"]
    user = User.objects.filter(username=username)
    if len(user) < 1:
        user = User.objects.create_user(username=username, password=password)
        if user is None:
            return render(request, "orders/register.html", {"message": "Invalid credentials."})
    else:
        user = user[0]
        user.is_active = True
        user.set_password(password)
        user.save()

    login(request, user)
    
    return HttpResponseRedirect(reverse("index"))


def unregister_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "orders/unregister.html")

    if request.POST["confirm-cancel"] == "confirm":
        request.user.is_active = False
        request.user.save()
        logout(request)

    return HttpResponseRedirect(reverse("index"))


def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    dishes = to_dict_list(Dish.objects, 'sort_number')

    put_columns_to_dishes(dishes)

    context = {
        "dishes": dishes,
    }
    return render(request, "orders/menu.html", context)


def put_columns_to_dishes(dishes):
    for dish in dishes:
#        put_types_columns(dish)

        flavors_columns = {}
        put_flavors(flavors_columns, dish)
        dish['flavors_columns'] = flavors_columns

#        put_addings_columns(dish)
#        put_sizes_columns(dish)



"""
def put_types_columns(table):
    for type in table.types:
#        put_flavors_columns(type)
#        put_addings_columns(type)
#        put_sizes_columns(type)
"""

def put_flavors(columns, table):
    sizes = []
    for flavor in table['flavors']:
#        put_addings_columns(flavor)

        put_sizes(sizes, flavor)
    
    columns['sizes'] = sizes


"""
def put_addings_columns(table):
    for adding in table.addings:
#        put_flavors(adding)
#        put_sizes_columns(adding)
"""

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
def get_dishes():
    items_db = Dish.objects.all().order_by('sort_number')
    items = json.loads(serializers.serialize("json", items_db))
    print(items)
    for (item_db, item) in zip(items_db, items):
        types = get_dish_types(item_db)
        item['fields']['types'] = types

    return items


def get_dish_types(dish):
    types = dish.types.all().order_by('sort_number')
        
    return types
"""

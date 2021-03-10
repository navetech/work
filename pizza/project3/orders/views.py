from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Size, SizeAndPrice
from .models import Dish, DishAdding, DishType
from .models import AddingFlavor, TypeFlavor
from .models import OrderStatus, Order, DishOrder


# Create your views here.

NO_ELEMENT = None
ALL_ELEMENTS = None


def index(request):
    #return HttpResponse("Project 3: TODO")

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("menu"))


def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    dishes_ids = ALL_ELEMENTS

    types_ids = ALL_ELEMENTS
    type_flavors_ids = ALL_ELEMENTS
    type_flavor_sizes_ids = ALL_ELEMENTS

    addings_ids = ALL_ELEMENTS
    adding_flavors_ids = ALL_ELEMENTS
    adding_flavor_sizes_ids = ALL_ELEMENTS

    view_dishes = get_view_dishes(dishes_ids,
        types_ids, type_flavors_ids, type_flavor_sizes_ids,
        addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    context = {
        "dishes": view_dishes,
    }
    return render(request, "orders/menu.html", context)


def flavor_view(request, dish_id, type_id, flavor_id, size_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    dishes_ids = [dish_id]

    types_ids = [type_id]
    type_flavors_ids = [flavor_id]
    type_flavor_sizes_ids = [size_id]

    addings_ids = ALL_ELEMENTS
    adding_flavors_ids = ALL_ELEMENTS
    adding_flavor_sizes_ids = ALL_ELEMENTS

    view_dishes = get_view_dishes(dishes_ids,
        types_ids, type_flavors_ids, type_flavor_sizes_ids,
        addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    dish = view_dishes[0]
    type_ = dish["types"][0]
    flavor = type_["flavors"][0]

    context = {
        "dish": dish["self"],
        "dish_addings": dish["addings"],
        "type": type_["self"],
        "type_sizes": type_["sizes"],
        "flavor": flavor["self"],
        "flavor_sizes_and_prices": flavor["sizes_and_prices"],
        "flavor_addings": flavor["addings"],
    }
    return render(request, "orders/flavor.html", context)


def get_view_dishes(dishes_ids,
        types_ids, type_flavors_ids, type_flavor_sizes_ids,
        addings_ids, adding_flavors_ids, adding_flavor_sizes_ids):

    dishes =  get_table_elements(table=Dish.objects,
        super_element=NO_ELEMENT, elements_ids=dishes_ids)

    if len(dishes) > 1:
        types_ids = ALL_ELEMENTS
        addings_ids = ALL_ELEMENTS

    view_dishes = []
    for dish in dishes:
        type_table = DishType.objects
        flavor_table = TypeFlavor.objects
        view_types = get_view_types_or_addings(type_table, flavor_table, dish,
            types_ids, type_flavors_ids, type_flavor_sizes_ids)

        adding_table = DishAdding.objects
        flavor_table = AddingFlavor.objects
        view_addings = get_view_types_or_addings(adding_table, flavor_table, dish,
            addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

        view_dishes.append({
        "self": dish,
        "types": view_types,
        "addings": view_addings,
        })
    return view_dishes


def get_table_elements(table, super_element, elements_ids):
    elements = []
    if elements_ids is ALL_ELEMENTS:
        if super_element is NO_ELEMENT:
            elements = table.all().order_by("sort_number")
        else:
            elements = table.filter(super=super_element).order_by("sort_number")
    else:
        for id in elements_ids:
            element = table.filter(pk=id)[0]
            if element:
                elements.append(element)
    return elements


def get_view_types_or_addings(type_or_adding_table, flavor_table, dish,
        types_or_addings_ids, flavors_ids, flavor_sizes_ids):

    types_or_addings =  get_table_elements(table=type_or_adding_table,
        super_element=dish, elements_ids=types_or_addings_ids)

    if len(types_or_addings) > 1:
        flavors_ids = ALL_ELEMENTS

    view_types_or_addings = []
    for type_or_adding in types_or_addings:
        flavors =  get_table_elements(table=flavor_table,
            super_element=type_or_adding, elements_ids=flavors_ids)

        type_or_adding_sizes = get_type_or_adding_sizes(flavors, flavor_sizes_ids)
        view_flavors = get_view_flavors(flavors, flavor_sizes_ids, type_or_adding_sizes)

        view_types_or_addings.append({
            "self": type_or_adding,
            "sizes": type_or_adding_sizes,
            "flavors": view_flavors,
        })
    return view_types_or_addings


def get_type_or_adding_sizes(flavors, flavor_sizes_ids):
    if len(flavors) > 1:
        flavor_sizes_ids = ALL_ELEMENTS

    all_sizes = Size.objects.all().order_by("sort_number")
    inside_type_or_adding_sizes = []
    for size in all_sizes:
        inside_size = {
            "size": size,
            "inside": False,
        }
        inside_type_or_adding_sizes.append(inside_size)

    for flavor in flavors:
        flavor_sizes = get_flavor_sizes(flavor, flavor_sizes_ids)
        for flavor_size in flavor_sizes:
            for inside_size in inside_type_or_adding_sizes:
                if flavor_size == inside_size["size"]:
                    inside_size["inside"] = True
                    break

    type_or_adding_sizes = []
    for inside_size in inside_type_or_adding_sizes:
        if inside_size["inside"]:
            type_or_adding_sizes.append(inside_size["size"])
    return type_or_adding_sizes


def get_flavor_sizes(flavor, flavor_sizes_ids):
    flavor_sizes = []
    sizes_and_prices = flavor.sizes_and_prices.all()
    if flavor_sizes_ids is ALL_ELEMENTS:
        for size_and_price in sizes_and_prices:
            flavor_sizes.append(size_and_price.size)
    else:
        for id in flavor_sizes_ids:
            size = Size.objects.filter(pk=id)[0]
            if size:
                for size_and_price in sizes_and_prices:
                    if size == size_and_price.size:
                        flavor_sizes.append(size_and_price.size)
    return flavor_sizes


def get_view_flavors(flavors, flavor_sizes_ids, type_or_adding_sizes):
    view_flavors = []
    for flavor in flavors:
        flavor_addings = []
        if hasattr(flavor, "addings"):
            flavor_addings = flavor.addings.all()

        view_sizes_and_prices = []
        for size in type_or_adding_sizes:
            view_size_and_price = {
                "size": size,
                "price": None,
            }
            view_sizes_and_prices.append(view_size_and_price)

        flavor_sizes_and_prices = get_flavor_sizes_and_prices(flavor, flavor_sizes_ids)
        for flavor_size_and_price in flavor_sizes_and_prices:
            for view_size_and_price in view_sizes_and_prices:
                if flavor_size_and_price.size == view_size_and_price["size"]:
                    view_size_and_price["price"] = flavor_size_and_price.price
                    break

        view_flavors.append({
            "self": flavor,
            "sizes_and_prices": view_sizes_and_prices,
            "addings": flavor_addings,
        })
    return view_flavors


def get_flavor_sizes_and_prices(flavor, flavor_sizes_ids):
    flavor_sizes_and_prices = []
    sizes_and_prices = flavor.sizes_and_prices.all()
    if flavor_sizes_ids is ALL_ELEMENTS:
        for size_and_price in sizes_and_prices:
            flavor_sizes_and_prices.append(size_and_price)
    else:
        for id in flavor_sizes_ids:
            size = Size.objects.filter(pk=id)[0]
            if size:
                for size_and_price in sizes_and_prices:
                    if size == size_and_price.size:
                        flavor_sizes_and_prices.append(size_and_price)
    return flavor_sizes_and_prices


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

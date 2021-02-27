from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Dish, Adding
from .models import Size
from .models import Topping, SpecialPizza, PizzaType, PizzaFlavor, Pizza
from .models import SubFlavor, Sub, ExtraFlavor, Extra
from .models import PastaFlavor, Pasta
from .models import SaladFlavor, Salad
from .models import DinnerPlatterFlavor, DinnerPlatter
from .models import OrderStatus, Order
from .models import PizzaOrder, SubOrder, PastaOrder, SaladOrder, DinnerPlatterOrder


# Create your views here.
def index(request):
    #return HttpResponse("Project 3: TODO")

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("menu"))


def menu_(request):
    menu_dishes = []

    dish_sizes = Size.objects.all().order_by("sort_number")

    dish = Dish.objects.filter(name="Pizzas")[0]
    dish_menu = []
    if dish is not None:
        dish_menu = pizzas_menu(dish_sizes)

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    dish = Dish.objects.filter(name="Subs")[0]
    dish_menu = []
    if dish is not None:
        dish_menu = subs_menu(dish_sizes)

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    dish = Dish.objects.filter(name="Pasta")[0]
    dish_menu = []
    if dish is not None:
        dish_menu = pastas_menu()

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    dish = Dish.objects.filter(name="Salads")[0]
    dish_menu = []
    if dish is not None:
        dish_menu = salads_menu()

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    dish = Dish.objects.filter(name="Dinner Platters")[0]
    dish_menu = []
    if dish is not None:
        dish_menu = dinnerplatters_menu(dish_sizes)

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })

    context = {
        "menu_dishes": menu_dishes,
    }
    return render(request, "orders/menu.html", context)


def pizzas_menu(dish_sizes):
    menu_types = []
    dish_types = PizzaType.objects.all().order_by("sort_number")
    if dish_types:
        flavors = PizzaFlavor.objects.all().order_by("sort_number")
        items = Pizza.objects.all()
        menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []
    addings = Adding.objects.filter(name="Toppings")
    if addings:
        flavors = Topping.objects.all().order_by("sort_number")
        items = []
        addings_sizes = []
        menu_addings = types_menu(addings, flavors, items, addings_sizes)

    return {
        "types": menu_types,
        "addings": menu_addings,
    }


def subs_menu(dish_sizes):
    dish_types = [None]

    flavors = SubFlavor.objects.all().order_by("sort_number")
    items = Sub.objects.all()
    menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []
    addings = Adding.objects.filter(name="Extras")
    if addings:
        flavors = ExtraFlavor.objects.all().order_by("sort_number")
        items = Extra.objects.all()
        addings_sizes = [None]
        menu_addings = types_menu(addings, flavors, items, addings_sizes)

    return {
        "types": menu_types,
        "addings": menu_addings,
    }


def pastas_menu():
    dish_types = [None]
    flavors = PastaFlavor.objects.all().order_by("sort_number")
    items = Pasta.objects.all()
    dish_sizes = [None]
    menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []

    return {
        "types": menu_types,
        "addings": menu_addings,
    }


def salads_menu():
    dish_types = [None]
    flavors = SaladFlavor.objects.all().order_by("sort_number")
    items = Salad.objects.all()
    dish_sizes = [None]
    menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []

    return {
        "types": menu_types,
        "addings": menu_addings,
    }


def dinnerplatters_menu(dish_sizes):
    dish_types = [None]

    flavors = DinnerPlatterFlavor.objects.all().order_by("sort_number")
    items = DinnerPlatter.objects.all()
    menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []

    return {
        "types": menu_types,
        "addings": menu_addings,
    }


def types_menu(dish_types, flavors, items, dish_sizes):
    menu_types = []
    for dish_type in dish_types:
        type_sizes = get_type_sizes(dish_type, flavors, items, dish_sizes)
        type_flavors = get_type_flavors(dish_type, flavors, items, type_sizes)
        if type_flavors:
            menu_types.append({
                "type": dish_type,
                "flavors": type_flavors,
                "sizes": type_sizes,
            })
    return menu_types


def get_type_sizes(dish_type, flavors, items, dish_sizes):
    type_sizes = []
    for dish_size in dish_sizes:
        for flavor in flavors:
            for item in items:
                if item:
                    has_attr = hasattr(item, "type")
                    if (dish_type and has_attr and dish_type == item.type) or not dish_type or not has_attr:
                        has_attr = hasattr(item, "flavor")
                        if (flavor and has_attr and flavor == item.flavor) or not flavor or not has_attr:
                            has_attr = hasattr(item, "size")
                            if (dish_size and has_attr and dish_size == item.size) or not dish_size or not has_attr:
                                if not dish_size in type_sizes:
                                    type_sizes.append(dish_size)
                                break
    return type_sizes


def get_type_flavors(dish_type, flavors, items, type_sizes):
    type_flavors = []
    for flavor in flavors:
        flavor_prices = []
        for dish_size in type_sizes:
            flavor_price = {
                "size": dish_size,
                "price": None,
            }
            for item in items:
                if item:
                    has_attr = hasattr(item, "type")
                    if (dish_type and has_attr and dish_type == item.type) or not dish_type or not has_attr:
                        has_attr = hasattr(item, "flavor")
                        if (flavor and has_attr and flavor == item.flavor) or not flavor or not has_attr:
                            has_attr = hasattr(item, "size")
                            if (dish_size and has_attr and dish_size == item.size) or not dish_size or not has_attr:
                                flavor_price = {
                                    "size": dish_size,
                                    "price": item.price,
                                }
                                break
            flavor_prices.append(flavor_price)

        if flavor_prices:
            for flavor_price in flavor_prices:
                if flavor_price and flavor_price["price"]:
                    type_flavors.append({
                        "flavor": flavor,
                        "prices": flavor_prices,
                    })
                    break
        else:
            type_flavors.append({
                "flavor": flavor,
                "prices": flavor_prices,
            })
    return type_flavors


def flavor_view(request, dish_id, type_id, flavor_id):
    dishes_ids = [dish_id]
    types_ids = [type_id]
    addings_ids = None
    flavors_ids = [flavor_id]
    sizes_ids = None
    view_dishes = build_view_dishes(dishes_ids, types_ids, addings_ids, flavors_ids, sizes_ids)

    context = {
        "dishes": view_dishes,
    }
    return render(request, "orders/flavor.html", context)


def menu(request):
    dishes_ids = None
    types_ids = None
    addings_ids = None
    flavors_ids = None
    sizes_ids = None
    view_dishes = build_view_dishes(dishes_ids, types_ids, addings_ids, flavors_ids, sizes_ids)

    context = {
        "dishes": view_dishes,
    }
    return render(request, "orders/menu.html", context)


def build_view_dishes(dishes_ids, types_ids, addings_ids, flavors_ids, sizes_ids):
    dishes = []
    if dishes_ids is None:
        dishes = Dish.objects.all().order_by("sort_number")
    else:
        for dish_id in dishes_ids:
            dish = Dish.objects.filter(pk=dish_id)[0]
            if dish:
                dishes.append(dish)

    view_dishes = []
    for dish in dishes:
        if dish.name == "Pizzas":
            view = build_pizzas_view(types_ids, addings_ids, flavors_ids, sizes_ids)
            view_dishes.append({
                "self": dish,
                "view": view,
            })
    return view_dishes

"""        elif dish.name == "Subs":
            view = subs_view(types_ids, addings_ids, flavors_ids, sizes_ids)
            views.append({
                "dish": dish,
                "view": view,
            })
        elif dish.name == "Pasta":
            view = pastas_view(types_ids, addings_ids, flavors_ids, sizes_ids)
            views.append({
                "dish": dish,
                "view": view,
            })
        elif dish.name == "Salads":
            view = salads_view(types_ids, addings_ids, flavors_ids, sizes_ids)
            views.append({
                "dish": dish,
                "view": view,
            })
        elif dish.name == "Dinner Platters":
            view = dinnerplaters_view(types_ids, addings_ids, flavors_ids, sizes_ids)
            views.append({
                "dish": dish,
                "view": view,
            })
"""


def build_pizzas_view(types_ids, addings_ids, flavors_ids, sizes_ids):
    types = []
    if types_ids is None:
        types = PizzaType.objects.all().order_by("sort_number")
    else:
        for id in types_ids:
            type = PizzaType.objects.filter(pk=id)[0]
            if type:
                types.append(type)

    types_view = []
    if types:
        flavors = []
        if flavors_ids is None:
            flavors = PizzaFlavor.objects.all().order_by("sort_number")
        else:
            for id in flavors_ids:
                flavor = PizzaFlavor.objects.filter(pk=id)[0]
                if flavor:
                    flavors.append(flavor)

        items = Pizza.objects.all()

        sizes = []
        if sizes_ids is None:
            sizes = Size.objects.all().order_by("sort_number")
        else:
            for id in sizes_ids:
                size = Size.objects.filter(pk=id)[0]
                if size:
                    sizes.append(size)

        types_view = build_types_or_addings_view(types, flavors, items, sizes)


    addings = []
    if addings_ids is None:
        addings = Adding.objects.filter(name="Toppings")
    else:
        for id in addings_ids:
            adding = Adding.objects.filter(pk=id)[0]
            if adding:
                addings.append(adding)

    addings_view = []
    if addings:
        flavors = []
        if flavors_ids is None:
            flavors = Topping.objects.all().order_by("sort_number")
        else:
            for id in flavors_ids:
                flavor = Topping.objects.filter(pk=id)[0]
                if flavor:
                    flavors.append(flavor)

        items = []
        sizes = []

        addings_view = build_types_or_addings_view(addings, flavors, items, sizes)

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_types_or_addings_view(types_or_addings, dish_flavors, items, dish_sizes):
    types_or_addings_view = []
    for type_or_adding in types_or_addings:
        type_or_adding_sizes = get_type_or_adding_sizes(type_or_adding, dish_flavors, items, dish_sizes)
        type_or_adding_flavors = get_type_or_adding_flavors(type_or_adding, dish_flavors, items, type_or_adding_sizes)
        if type_or_adding_flavors:
            types_or_addings_view.append({
                "self": type_or_adding,
                "flavors": type_or_adding_flavors,
                "sizes": type_or_adding_sizes,
            })
    return types_or_addings_view


def get_type_or_adding_sizes(type_or_adding, dish_flavors, items, dish_sizes):
    type_or_adding_sizes = []
    for size in dish_sizes:
        for flavor in dish_flavors:
            for item in items:
                if item:
                    has_attr = hasattr(item, "type")
                    if (type_or_adding and has_attr and type_or_adding == item.type) or not type_or_adding or not has_attr:
                        has_attr = hasattr(item, "flavor")
                        if (flavor and has_attr and flavor == item.flavor) or not flavor or not has_attr:
                            has_attr = hasattr(item, "size")
                            if (size and has_attr and size == item.size) or not size or not has_attr:
                                if not size in type_or_adding_sizes:
                                    type_or_adding_sizes.append(size)
                                break
    return type_or_adding_sizes


def get_type_or_adding_flavors(type_or_adding, dish_flavors, items, type_or_adding_sizes):
    type_or_adding_flavors = []
    for flavor in dish_flavors:
        flavor_sizes_and_prices = []
        for size in type_or_adding_sizes:
            size_and_price = {
                "size": size,
                "price": None,
            }
            for item in items:
                if item:
                    has_attr = hasattr(item, "type")
                    if (type_or_adding and has_attr and type_or_adding == item.type) or not type_or_adding or not has_attr:
                        has_attr = hasattr(item, "flavor")
                        if (flavor and has_attr and flavor == item.flavor) or not flavor or not has_attr:
                            has_attr = hasattr(item, "size")
                            if (size and has_attr and size == item.size) or not size or not has_attr:
                                size_and_price = {
                                    "size": size,
                                    "price": item.price,
                                }
                                break
            flavor_sizes_and_prices.append(size_and_price)

        if flavor_sizes_and_prices:
            for size_and_price in flavor_sizes_and_prices:
                if size_and_price and size_and_price["price"]:
                    type_or_adding_flavors.append({
                        "self": flavor,
                        "sizes_and_prices": flavor_sizes_and_prices,
                    })
                    break
        else:
            type_or_adding_flavors.append({
                "self": flavor,
                "sizes_and_prices": flavor_sizes_and_prices,
            })
    return type_or_adding_flavors



def login_view(request):
    if request.method == "GET":
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
        return render(request, "orders/unregister.html")

    if request.POST["confirm-cancel"] == "confirm":
        request.user.is_active = False
        request.user.save()
        logout(request)

    return HttpResponseRedirect(reverse("index"))

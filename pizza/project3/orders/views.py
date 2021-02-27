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

ALL_DISHES = None
ALL_TYPES = None
ALL_ADDINGS = None
ALL_FLAVORS = None
ALL_SIZES = None

UNDEFINED_TYPE = None
UNDEFINED_SIZE = None


def index(request):
    #return HttpResponse("Project 3: TODO")

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("menu"))


def menu(request):
    dishes_ids = ALL_DISHES
    types_ids = ALL_TYPES
    addings_ids = ALL_ADDINGS
    flavors_ids = ALL_FLAVORS
    sizes_ids = ALL_SIZES
    dishes_view = build_dishes_view(dishes_ids, types_ids, addings_ids, flavors_ids, sizes_ids)

    context = {
        "dishes": dishes_view,
    }
    return render(request, "orders/menu.html", context)


def flavor_view(request, dish_id, type_id, flavor_id):
    dishes_ids = [dish_id]
    types_ids = [type_id]
    addings_ids = ALL_ADDINGS
    flavors_ids = [flavor_id]
    sizes_ids = ALL_SIZES
    dishes_view = build_dishes_view(dishes_ids, types_ids, addings_ids, flavors_ids, sizes_ids)

    context = {
        "dishes": dishes_view,
    }
    return render(request, "orders/flavor.html", context)


def build_dishes_view(dishes_ids, types_ids, addings_ids, flavors_ids, sizes_ids):
    dishes = []
    if dishes_ids is ALL_DISHES:
        dishes = Dish.objects.all().order_by("sort_number")
    else:
        for dish_id in dishes_ids:
            dish = Dish.objects.filter(pk=dish_id)[0]
            if dish:
                dishes.append(dish)

    dishes_view = []
    for dish in dishes:
        view = None
        if dish.name == "Pizzas":
            view = build_pizzas_view(types_ids, addings_ids, flavors_ids, sizes_ids)
        elif dish.name == "Subs":
            view = build_subs_view(addings_ids, flavors_ids, sizes_ids)
        elif dish.name == "Pasta":
            view = build_pastas_view(flavors_ids)
        elif dish.name == "Salads":
            view = build_salads_view(flavors_ids)
        elif dish.name == "Dinner Platters":
            view = build_dinnerplatters_view(flavors_ids, sizes_ids)

        if view is not None:
            dishes_view.append({
                "self": dish,
                "view": view,
            })

    return dishes_view


def build_pizzas_view(types_ids, addings_ids, flavors_ids, sizes_ids):
    types_view = []

    types = []
    if types_ids is ALL_TYPES:
        types = PizzaType.objects.all().order_by("sort_number")
    else:
        for id in types_ids:
            type = PizzaType.objects.filter(pk=id)[0]
            if type:
                types.append(type)

    if types:
        flavors = []
        if flavors_ids is ALL_FLAVORS:
            flavors = PizzaFlavor.objects.all().order_by("sort_number")
        else:
            for id in flavors_ids:
                flavor = PizzaFlavor.objects.filter(pk=id)[0]
                if flavor:
                    flavors.append(flavor)

        items = Pizza.objects.all()

        sizes = []
        if sizes_ids is ALL_SIZES:
            sizes = Size.objects.all().order_by("sort_number")
        else:
            for id in sizes_ids:
                size = Size.objects.filter(pk=id)[0]
                if size:
                    sizes.append(size)

        types_view = build_types_or_addings_view(types, flavors, items, sizes)

    addings_view = []

    addings = []
    if addings_ids is ALL_ADDINGS:
        addings = Adding.objects.filter(name="Toppings")
    else:
        for id in addings_ids:
            adding = Adding.objects.filter(pk=id)[0]
            if adding:
                addings.append(adding)

    if addings:
        flavors = Topping.objects.all().order_by("sort_number")
        items = []
        sizes = []

        addings_view = build_types_or_addings_view(addings, flavors, items, sizes)

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_subs_view(addings_ids, flavors_ids, sizes_ids):
    types_view = []

    types = [UNDEFINED_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = SubFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = SubFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)

    items = Sub.objects.all()

    sizes = []
    if sizes_ids is ALL_SIZES:
        sizes = Size.objects.all().order_by("sort_number")
    else:
        for id in sizes_ids:
            size = Size.objects.filter(pk=id)[0]
            if size:
                sizes.append(size)

    types_view = build_types_or_addings_view(types, flavors, items, sizes)

    addings_view = []

    addings = []
    if addings_ids is ALL_ADDINGS:
        addings = Adding.objects.filter(name="Extras")
    else:
        for id in addings_ids:
            adding = Adding.objects.filter(pk=id)[0]
            if adding:
                addings.append(adding)

    if addings:
        flavors = ExtraFlavor.objects.all().order_by("sort_number")
        items = Extra.objects.all()
        sizes = [UNDEFINED_SIZE]

        addings_view = build_types_or_addings_view(addings, flavors, items, sizes)

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_pastas_view(flavors_ids):
    types_view = []

    types = [UNDEFINED_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = PastaFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = PastaFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)

    items = Pasta.objects.all()

    sizes = [UNDEFINED_SIZE]

    types_view = build_types_or_addings_view(types, flavors, items, sizes)

    addings_view = []

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_salads_view(flavors_ids):
    types_view = []

    types = [UNDEFINED_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = SaladFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = SaladFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)

    items = Salad.objects.all()

    sizes = [UNDEFINED_SIZE]

    types_view = build_types_or_addings_view(types, flavors, items, sizes)

    addings_view = []

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_dinnerplatters_view(flavors_ids, sizes_ids):
    types_view = []

    types = [UNDEFINED_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = DinnerPlatterFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = DinnerPlatterFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)

    items = DinnerPlatter.objects.all()

    sizes = []
    if sizes_ids is ALL_SIZES:
        sizes = Size.objects.all().order_by("sort_number")
    else:
        for id in sizes_ids:
            size = Size.objects.filter(pk=id)[0]
            if size:
                sizes.append(size)

    types_view = build_types_or_addings_view(types, flavors, items, sizes)

    addings_view = []

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

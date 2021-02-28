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

GENERIC_TYPE = None
ONE_SIZE = None


def index(request):
    #return HttpResponse("Project 3: TODO")

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("menu"))


def menu(request):
    dishes_ids = ALL_DISHES

    types_ids = ALL_TYPES
    type_flavors_ids = ALL_FLAVORS
    type_flavor_sizes_ids = ALL_SIZES

    addings_ids = ALL_ADDINGS
    adding_flavors_ids = ALL_FLAVORS
    adding_flavor_sizes_ids = ALL_SIZES

    dishes_view = build_dishes_view(dishes_ids, types_ids, type_flavors_ids, type_flavor_sizes_ids,
        addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    context = {
        "dishes": dishes_view,
    }
    return render(request, "orders/menu.html", context)


def flavor_view(request, dish_id, type_id, flavor_id):
    dishes_ids = [dish_id]

    types_ids = [type_id]
    type_flavors_ids = [flavor_id]
    type_flavor_sizes_ids = ALL_SIZES

    addings_ids = ALL_ADDINGS
    adding_flavors_ids = ALL_FLAVORS
    adding_flavor_sizes_ids = ALL_SIZES

    dishes_view = build_dishes_view(dishes_ids, types_ids, type_flavors_ids, type_flavor_sizes_ids,
        addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    context = {
        "dishes": dishes_view,
    }
    return render(request, "orders/flavor.html", context)


def build_dishes_view(dishes_ids=ALL_DISHES,
    types_ids=ALL_TYPES, type_flavors_ids=ALL_FLAVORS, type_flavor_sizes_ids=ALL_SIZES,
    addings_ids=ALL_ADDINGS, adding_flavors_ids=ALL_FLAVORS, adding_flavor_sizes_ids=ALL_SIZES):

    dishes = []
    if dishes_ids is ALL_DISHES:
        dishes = Dish.objects.all().order_by("sort_number")
    else:
        for dish_id in dishes_ids:
            dish = Dish.objects.filter(pk=dish_id)[0]
            if dish:
                dishes.append(dish)
    if len(dishes) > 1:
        types_ids = ALL_TYPES
        addings_ids = ALL_ADDINGS

    dishes_view = []
    for dish in dishes:
        view = None
        if dish.name == "Pizzas":
            view = build_pizzas_view(types_ids, type_flavors_ids, type_flavor_sizes_ids,
                addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)
        elif dish.name == "Subs":
            view = build_subs_view(type_flavors_ids, type_flavor_sizes_ids,
                addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)
        elif dish.name == "Pasta":
            view = build_pastas_view(type_flavors_ids)
        elif dish.name == "Salads":
            view = build_salads_view(type_flavors_ids)
        elif dish.name == "Dinner Platters":
            view = build_dinnerplatters_view(type_flavors_ids, type_flavor_sizes_ids)

        if view is not None:
            dishes_view.append({
                "self": dish,
                "view": view,
            })

    return dishes_view


def build_pizzas_view(types_ids=ALL_TYPES, type_flavors_ids=ALL_FLAVORS, type_flavor_sizes_ids=ALL_SIZES,
    addings_ids=ALL_ADDINGS, adding_flavors_ids=ALL_FLAVORS, adding_flavor_sizes_ids=ALL_SIZES):

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
        if len(types) > 1:
            type_flavors_ids = ALL_FLAVORS

        flavors = []
        if type_flavors_ids is ALL_FLAVORS:
            flavors = PizzaFlavor.objects.all().order_by("sort_number")
        else:
            for id in type_flavors_ids:
                flavor = PizzaFlavor.objects.filter(pk=id)[0]
                if flavor:
                    flavors.append(flavor)
        if flavors:
            items = Pizza.objects.all()

            if len(flavors) > 1:
                type_flavor_sizes_ids = ALL_SIZES

            sizes = []
            if type_flavor_sizes_ids is ALL_SIZES:
                sizes = Size.objects.all().order_by("sort_number")
            else:
                for id in type_flavor_sizes_ids:
                    size = Size.objects.filter(pk=id)[0]
                    if size:
                        sizes.append(size)

            if sizes:
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
        if len(addings) > 1:
            adding_flavors_ids = ALL_FLAVORS

        flavors = []
        if adding_flavors_ids is ALL_FLAVORS:
            flavors = Topping.objects.all().order_by("sort_number")
        else:
            for id in adding_flavors_ids:
                flavor = Topping.objects.filter(pk=id)[0]
                if flavor:
                    flavors.append(flavor)
        if flavors:
            items = []
            sizes = []

            addings_view = build_types_or_addings_view(addings, flavors, items, sizes)

    return {
        "types": types_view,
        "addings": addings_view,
    }

def build_subs_view(flavors_ids=ALL_FLAVORS, flavor_sizes_ids=ALL_SIZES,
    addings_ids=ALL_ADDINGS, adding_flavors_ids=ALL_FLAVORS, adding_flavor_sizes_ids=ALL_SIZES):

    types_view = []

    types = [GENERIC_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = SubFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = SubFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if flavors:
        items = Sub.objects.all()

        if len(flavors) > 1:
            flavor_sizes_ids = ALL_SIZES

        sizes = []
        if flavor_sizes_ids is ALL_SIZES:
            sizes = Size.objects.all().order_by("sort_number")
        else:
            for id in flavor_sizes_ids:
                size = Size.objects.filter(pk=id)[0]
                if size:
                    sizes.append(size)
        if sizes:
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
        if len(addings) > 1:
            adding_flavors_ids = ALL_FLAVORS

        flavors = []
        if adding_flavors_ids is ALL_FLAVORS:
            flavors = ExtraFlavor.objects.all().order_by("sort_number")
        else:
            for id in adding_flavors_ids:
                flavor = ExtraFlavor.objects.filter(pk=id)[0]
                if flavor:
                    flavors.append(flavor)
        if flavors:
            items = Extra.objects.all()
            sizes = [ONE_SIZE]

            addings_view = build_types_or_addings_view(addings, flavors, items, sizes)

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_pastas_view(flavors_ids=ALL_FLAVORS):
    types_view = []

    types = [GENERIC_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = PastaFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = PastaFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if flavors:
        items = Pasta.objects.all()
        sizes = [ONE_SIZE]

        types_view = build_types_or_addings_view(types, flavors, items, sizes)

    addings_view = []

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_salads_view(flavors_ids=ALL_FLAVORS):
    types_view = []

    types = [GENERIC_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = SaladFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = SaladFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if flavors:
        items = Salad.objects.all()
        sizes = [ONE_SIZE]

        types_view = build_types_or_addings_view(types, flavors, items, sizes)
        
    addings_view = []

    return {
        "types": types_view,
        "addings": addings_view,
    }


def build_dinnerplatters_view(flavors_ids=ALL_FLAVORS, flavor_sizes_ids=ALL_SIZES):
    types_view = []

    types = [GENERIC_TYPE]

    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = DinnerPlatterFlavor.objects.all().order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = DinnerPlatterFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if flavors:
        items = DinnerPlatter.objects.all()

        if len(flavors) > 1:
            flavor_sizes_ids = ALL_SIZES

        sizes = []
        if flavor_sizes_ids is ALL_SIZES:
            sizes = Size.objects.all().order_by("sort_number")
        else:
            for id in flavor_sizes_ids:
                size = Size.objects.filter(pk=id)[0]
                if size:
                    sizes.append(size)
        if sizes:
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

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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    dishes_ids = ALL_DISHES

    types_ids = ALL_TYPES
    type_flavors_ids = ALL_FLAVORS
    type_flavor_sizes_ids = ALL_SIZES

    addings_ids = ALL_ADDINGS
    adding_flavors_ids = ALL_FLAVORS
    adding_flavor_sizes_ids = ALL_SIZES

    dishes_view = build_dishes_view(dishes_ids,
        types_ids, type_flavors_ids, type_flavor_sizes_ids,
        addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    context = {
        "dishes": dishes_view,
    }
    return render(request, "orders/menu.html", context)


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
        type_or_adding_table = DishType.objects
        flavor_table = TypeFlavor.objects
        types_view = build_types_or_addings_view(type_or_adding_table, flavor_table, dish,
            types_ids, type_flavors_ids, type_flavor_sizes_ids)

        type_or_adding_table = DishAdding.objects
        flavor_table = AddingFlavor.objects
        addings_view = build_types_or_addings_view(type_or_adding_table, flavor_table, dish,
            addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

#        types_view = build_types_view(dish, types_ids, type_flavors_ids, type_flavor_sizes_ids)
#        addings_view = build_addings_view(dish, addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)
        dishes_view.append({
            "self": dish,
            "types": types_view,
            "addings": addings_view,
        })

    return dishes_view


def build_types_or_addings_view(type_or_adding_table, flavor_table, dish,
        types_or_addings_ids, flavors_ids, flavor_sizes_ids):

    types_or_addings = []
    if types_or_addings_ids is ALL_TYPES:
        types_or_addings = type_or_adding_table.filter(dish=dish).order_by("sort_number")
    else:
        for id in types_or_addings_ids:
            type_or_adding = type_or_adding_table.filter(pk=id)[0]
            if type_or_adding:
                types_or_addings.append(type_or_adding)

    if len(types_or_addings) > 1:
        flavors_ids = ALL_FLAVORS

    types_or_addings_view = []
    for type_or_adding in types_or_addings:
        type_or_adding_sizes = get_type_or_adding_sizes(flavor_table, type_or_adding, flavors_ids, flavor_sizes_ids)
        flavors_view = build_flavors_view(flavor_table, type_or_adding, flavors_ids, flavor_sizes_ids)

        types_or_addings_view.append({
            "self": type_or_adding,
            "sizes": type_or_adding_sizes,
            "flavors": flavors_view,
        })

    return types_or_addings_view


def get_type_or_adding_sizes(flavor_table, type_or_adding, flavors_ids, flavor_sizes_ids):
    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = flavor_table.filter(type_or_adding=type_or_adding).order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = flavor_table.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if len(flavors) > 1:
        flavor_sizes_ids = ALL_SIZES

    all_sizes = Size.objects.all().order_by("sort_number")
    inside_sizes = []
    for size in all_sizes:
        inside_size = {
            "size": size,
            "inside": False,
        }
        inside_sizes.append(inside_size)

    for flavor in flavors:
        for flavor_size_price in flavor.sizes_and_prices:
            for inside_size in inside_sizes:
                if flavor_size_price.size == inside_size["size"]:
                    inside_size["inside"] = True
                    break

    type_or_adding_sizes = []
    for inside_size in inside_sizes:
        if inside_size["inside"]:
            type_or_adding_sizes.append(inside_size["size"])

    return type_or_adding_sizes


def build_flavors_view(flavor_table, type_or_adding, flavors_ids, flavor_sizes_ids):
    flavors = []
    if flavors_ids is ALL_FLAVORS:
        flavors = flavor_table.filter(type_or_adding=type_or_adding).order_by("sort_number")
    else:
        for id in flavors_ids:
            flavor = flavor_table.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if len(flavors) > 1:
        flavor_sizes_ids = ALL_SIZES

PAREI AQUI



"""
def build_types_view(dish, types_ids, type_flavors_ids, type_flavor_sizes_ids):
    types = []
    if types_ids is ALL_TYPES:
        types = DishType.objects.filter(dish=dish).order_by("sort_number")
    else:
        for id in types_ids:
            type = DishType.objects.filter(pk=id)[0]
            if type:
                types.append(type)
    if len(types) > 1:
        type_flavors_ids = ALL_FLAVORS

    types_view = []
    for type in types:
        type_sizes = []
        flavors_view = []
#        type_sizes = get_type_sizes(type, type_flavors_ids, type_flavor_sizes_ids)
#        flavors_view = build_type_flavors_view(type, type_flavors_ids, type_flavor_sizes_ids)
        types_view.append({
            "self": type,
            "sizes": type_sizes,
            "flavors": flavors_view,
        })

    return types_view


def build_addings_view(dish, addings_ids, adding_flavors_ids, adding_flavor_sizes_ids):
    addings = []
    if addings_ids is ALL_TYPES:
        addings = DishAdding.objects.filter(dish=dish).order_by("sort_number")
    else:
        for id in addings_ids:
            adding = DishAdding.objects.filter(pk=id)[0]
            if adding:
                types.append(adding)
    if len(addings) > 1:
        adding_flavors_ids = ALL_FLAVORS

    addings_view = []
    for adding in addings:
        adding_sizes = []
        flavors_view = []
#        type_sizes = get_type_sizes(type, type_flavors_ids, type_flavor_sizes_ids)
#        flavors_view = build_type_flavors_view(type, type_flavors_ids, type_flavor_sizes_ids)
        addings_view.append({
            "self": adding,
            "sizes": adding_sizes,
            "flavors": flavors_view,
        })

    return addings_view
"""


"""
def get_type_sizes(type, type_flavors_ids, type_flavor_sizes_ids):
    flavors = []
    if type_flavors_ids is ALL_FLAVORS:
        flavors = TypeFlavor.objects.filter(type=type).order_by("sort_number")
    else:
        for id in type_flavors_ids:
            flavor = TypeFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if len(flavors) > 1:
        type_flavor_sizes_ids = ALL_SIZES

def get_type_or_adding_sizes(type_or_adding, dish_flavors, items, dish_sizes):
    if not dish_sizes:
        return []

    inside_sizes = []
    for size in dish_sizes:
        inside_size = {
            "size": size,
            "inside": False,
        }
        inside_sizes.append(inside_size)

    for flavor in dish_flavors:
        for inside_size in inside_sizes:
            for item in items:
                if match(type_or_adding, flavor, inside_size["size"], item):
                    inside_size["inside"] = True
                    break

    type_or_adding_sizes = []
    for inside_size in inside_sizes:
        if inside_size["inside"]:
            type_or_adding_sizes.append(inside_size["size"])

    return type_or_adding_sizes
"""


def build_flavors_view(type, type_flavors_ids=ALL_FLAVORS, type_flavor_sizes_ids=ALL_SIZES):
    flavors = []
    if type_flavors_ids is ALL_FLAVORS:
        flavors = TypeFlavor.objects.filter(type=type).order_by("sort_number")
    else:
        for id in type_flavors_ids:
            flavor = TypeFlavor.objects.filter(pk=id)[0]
            if flavor:
                flavors.append(flavor)
    if len(flavors) > 1:
        type_flavor_sizes_ids = ALL_SIZES

    flavors_view = []
    for flavor in flavors:
        sizes_and_prices_view = build_sizes_and_prices_view(flavor, type_flavor_sizes_ids)
        flavors_view.append({
            "self": flavor,
            "sizes_and_prices": sizes_and_prices_view,
        })

    return flavors_view


"""
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
    flavors_view = []


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

    if types_view or addings_view:
        return {
            "types": types_view,
            "addings": addings_view,
        }
    else:
        return None




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
    if not dish_sizes:
        return []

    inside_sizes = []
    for size in dish_sizes:
        inside_size = {
            "size": size,
            "inside": False,
        }
        inside_sizes.append(inside_size)

    for flavor in dish_flavors:
        for inside_size in inside_sizes:
            for item in items:
                if match(type_or_adding, flavor, inside_size["size"], item):
                    inside_size["inside"] = True
                    break

    type_or_adding_sizes = []
    for inside_size in inside_sizes:
        if inside_size["inside"]:
            type_or_adding_sizes.append(inside_size["size"])

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
                if match(type_or_adding, flavor, size, item):
                    if hasattr(item, "price"):
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
            if items is None:
                type_or_adding_flavors.append({
                    "self": flavor,
                    "sizes_and_prices": flavor_sizes_and_prices,
                })
    return type_or_adding_flavors


def match(type, flavor, size, item):
    if not item:
        return False

    has_type = hasattr(item, "type")
    if has_type:
        item_type = item.type

    has_flavor = hasattr(item, "flavor")
    if has_flavor:
        item_flavor = item.flavor
        has_flavor_type = hasattr(item.flavor, "type")
        has_flavor_flavor = hasattr(item.flavor, "flavor")

        if has_flavor_type:
            has_type = True
            item_type = item.flavor.type
            if not has_flavor_flavor:
                has_flavor = False

    if (type and has_type and type == item_type) or not type or not has_type:
        if (flavor and has_flavor and flavor == item_flavor) or not flavor or not has_flavor:
            has_size = hasattr(item, "size")
            if (size and has_size and size == item.size) or not size or not has_size:
                return True
    return False
"""


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


"""


def flavor_view(request, dish_id, type_id, flavor_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

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

    if types_view or addings_view:
        return {
            "types": types_view,
            "addings": addings_view,
        }
    else:
        return None


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

    if types_view or addings_view:
        return {
            "types": types_view,
            "addings": addings_view,
        }
    else:
        return None


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

    if types_view or addings_view:
        return {
            "types": types_view,
            "addings": addings_view,
        }
    else:
        return None


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

    if types_view or addings_view:
        return {
            "types": types_view,
            "addings": addings_view,
        }
    else:
        return None
"""

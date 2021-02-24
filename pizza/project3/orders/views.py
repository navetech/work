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


def menu(request):
    menu_dishes = []

    dish_sizes = Size.objects.all().order_by("sort_number")

    dish = Dish.objects.filter(name="Pizzas")[0]
    dish_menu = []
    if dish is not None:
        dish_types = PizzaType.objects.all().order_by("sort_number")
        addings = Adding.objects.filter(name="Toppings")[0]
        dish_menu = pizzas_menu(dish_types, addings, dish_sizes)

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    dish = Dish.objects.filter(name="Subs")[0]
    dish_menu = []
    if dish is not None:
        addings = Adding.objects.filter(name="Extras")[0]
        dish_menu = subs_menu(addings, dish_sizes)

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    dish = Dish.objects.filter(name="Pasta")[0]
    dish_menu = []
    if dish is not None:
        pass
        dish_menu = pastas_menu()

    menu_dishes.append({
        "dish": dish,
        "menu": dish_menu,
    })


    context = {
        "menu_dishes": menu_dishes,
    }
    return render(request, "orders/menu.html", context)


def pizzas_menu(dish_types, addings, dish_sizes):
    menu_types = []
    if dish_types:
        flavors = PizzaFlavor.objects.all().order_by("sort_number")
        items = Pizza.objects.all()
        menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []
    if addings:
        menu_addings = Topping.objects.all()

    return {
        "types": menu_types,
        "addings": menu_addings,
    }


def subs_menu(addings, dish_sizes):
    dish_types = [None]
    flavors = SubFlavor.objects.all().order_by("sort_number")
    items = Sub.objects.all()
    menu_types = types_menu(dish_types, flavors, items, dish_sizes)

    menu_addings = []
    if addings:
        menu_addings = Extra.objects.all()

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


def types_menu(dish_types, flavors, items, dish_sizes):
    menu_types = []
    for dish_type in dish_types:
        type_sizes = []
        type_flavors = []
        for flavor in flavors:
            for dish_size in dish_sizes:
                for item in items:
                    if item is not None:
                        if (dish_type is not None and dish_type == item.dish_type) or dish_type is None:
                            if (flavor is not None and flavor == item.flavor) or flavor is None:
                                if dish_size is not None and dish_size == item.dish_size or dish_size is None:
                                    if not dish_size in type_sizes:
                                        type_sizes.append(dish_size)

                                    break

        for flavor in flavors:
            flavor_sizes = []
            for dish_size in type_sizes:
#                flavor_size = {}
#                if dish_size is not None:
                flavor_size = {
                    "size": dish_size,
                    "price": None,
                }
                for item in items:
                    if item is not None:
                        if (dish_type is not None and dish_type == item.dish_type) or dish_type is None:
                            if (flavor is not None and flavor == item.flavor) or flavor is None:
                                if dish_size is not None and dish_size == item.dish_size or dish_size is None:
                                    flavor_size = {
                                        "size": dish_size,
                                        "price": item.price,
                                    }

                                    break

                flavor_sizes.append(flavor_size)

            for flavor_size in flavor_sizes:
                if flavor_size is not None and flavor_size["price"] is not None:
                    type_flavors.append({
                        "flavor": flavor,
                        "sizes": flavor_sizes,
                    })
                    break

        if len(type_flavors) > 0 and len(type_sizes) > 0:
            menu_types.append({
                "type": dish_type,
                "flavors": type_flavors,
                "sizes": type_sizes,
            })

    return menu_types


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

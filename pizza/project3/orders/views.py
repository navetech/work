from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

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
    all_sizes = Size.objects.all()

    pizzas = pizzas_menu(all_sizes)
    toppings = toppings_menu()
    subs = subs_menu(all_sizes)
#    pastas = pastas_menu()
#    salads = salads_menu()
#    dinnerplatters = dinnerplatters_menu(all_sizes)

    context = {
        pizzas: pizzas,
        toppings: toppings,
        subs: subs,
#        pastas: pastas,
#        salads: salads,
#        dinnerplatters: dinnerplatters,
    }

    return render(request, "orders/menu.html", context)


def pizzas_menu(all_sizes):
    dish_types = PizzaType.objects.all()
    flavors = PizzaFlavor.objects.all()
    items = Pizza.objects.all()

    return dish_menu(dish_types, flavors, items, all_sizes)


def toppings_menu():
    return Topping.objects.all()


def subs_menu(all_sizes):
    dish_types = [None]
    flavors = SubFlavor.objects.all()
    items = Sub.objects.all()

    return dish_menu(dish_types, flavors, items, all_sizes)



def dish_menu(dish_types, flavors, items, all_sizes):
    dishes = []
    for dish_type in dish_types:
        type_flavors = []
        type_sizes = []
        for flavor in flavors:
            flavor_sizes = []
            for dish_size in all_sizes:
                for item in items:
                    if item is not None:
                        if (dish_type is not None and dish_type == item.dish_type) or dish_type is None:
                            if (flavor is not None and flavor == item.flavor) or flavor is None:
                                if dish_size is not None and dish_size == item.dish_size:
                                    flavor_sizes.append({
                                        "size": dish_size,
                                        "price": item.price,
                                    })

                                if not dish_size in type_sizes:
                                    type_sizes.append(dish_size)

                                break

            if len(flavor_sizes) > 0:
                type_flavors.append({
                    "flavor": flavor,
                    "sizes": flavor_sizes,
                })

        if len(type_flavors) > 0 and len(type_sizes) > 0:
            dishes.append({
                "type": dish_type,
                "flavors": type_flavors,
                "sizes": type_sizes,
            })

    return dishes


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

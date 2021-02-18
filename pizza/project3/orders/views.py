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
        item_types = PizzaType.objects.all()
        item_flavors = PizzaFlavor.objects.all()
        item_sizes = Size.objects.all()
        items = Pizza.objects.all()

        page_types_pizzas = []
        for item_type in item_types:

            page_flavors_types_items = []
            page_sizes_types_items = []
            for item_flavor in item_flavors:

                page_sizes_flavors_types_items = []
                for item_size in item_sizes:

                    for item in items:
                        if  item.pizza_type == item_type and item.flavor == item_flavor and item.pizza_size == item_size:
                            page_sizes_flavors_types_items.append({
                                "size": item_size,
                                "price": item.price,
                                })

                            if not {"size": item_size} in page_sizes_types_items:
                                page_sizes_types_items.append({
                                    "size": item_size,
                                })

                            break

                if len(page_sizes_flavors_types_items) > 0:
                    page_flavors_types_items.append({
                        "flavor": item_flavor,
                        "sizes": page_sizes_flavors_types_items,
                        })

            if len(page_flavors_types_items) > 0 and len(page_sizes_types_items) > 0:
                page_types_pizzas.append({
                "type": item_type,
                "flavors": page_flavors_types_items,
                "sizes": page_sizes_types_items,
                })


        toppings = Topping.objects.all()


        item_flavors = SubFlavor.objects.all()
        items = Sub.objects.all()

        page_flavors_subs = []
        page_sizes_subs = []
        for item_flavor in item_flavors:

            page_sizes_flavors_items = []
            for item_size in item_sizes:

                for item in items:
                    if item.flavor == item_flavor and item.sub_size == item_size:
                        page_sizes_flavors_items.append({
                                "size": item_size,
                                "price": item.price,
                                })

                        if not {"size": item_size} in page_sizes_subs:
                            page_sizes_subs.append({
                                "size": item_size,
                            })

                        break

            if len(page_sizes_flavors_items) > 0:
                page_flavors_subs.append({
                    "flavor": item_flavor,
                    "sizes": page_sizes_flavors_items,
                    })


        context = {
            "message": f"Hello, {request.user}",
            "types_pizzas": page_types_pizzas,
            "toppings": toppings,
            "flavors_subs": page_flavors_subs,
            "sizes_subs": page_sizes_subs,
        }
        return render(request, "orders/menu.html", context)


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

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
        sizes = Size.objects.all()
        pizza_types = PizzaType.objects.all()
        pizza_flavors = PizzaFlavor.objects.all()
        pizzas = Pizza.objects.all()
        context = {
            "message": f"Hello, {request.user}",
            "sizes": sizes,
            "pizza_types": pizza_types,
            "pizza_flavors": pizza_flavors,
            "pizzas": pizzas
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

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Size, SizeAndPrice
from .models import Dish, DishAdding, DishType
from .models import AddingFlavor, TypeFlavor
from .models import OrderStatus, Order
from .models import OrderItemAddingFlavorSizeAndPrice, OrderItemAddingFlavor
from .models import OrderItemAdding, OrderItem


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
        return HttpResponseRedirect(reverse("index"))

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


def ordering_view(request, flavor_id, size_id):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        order_item = get_order_item(request.user, flavor_id, size_id)

    else:
        order_item = get_order_item(request.user, flavor_id, size_id)

        if request.POST["submit"] == "inc-flavor-qty":
            order_item.qty += 1
            order_item.save()
        elif request.POST["submit"] == "dec-flavor-qty":
            if order_item.qty > 0:
                order_item.qty -= 1
                order_item.save()

        flavor = order_item.flavor
        if flavor.code <= 0:
            min_addings = 0
            max_addings = -flavor.code
        else:
            min_addings = flavor.code
            max_addings = flavor.code

        addings = order_item.addings.all()
        qty_addings = 0
        if order_item.qty <= 0:
            for adding in addings:
                flavors = adding.flavors.all()
                for flavor in flavors:
                    flavor.qty = 0
                    flavor.save()
                    sizes_and_prices = flavor.sizes_and_prices.all()
                    for size_and_price in sizes_and_prices:
                        size_and_price.qty = 0
                        size_and_price.save()
                    
        else:
            for adding in addings:
                flavors = adding.flavors.all()
                for flavor in flavors:
                    sizes_and_prices = flavor.sizes_and_prices.all()
                    if sizes_and_prices:
                        for size_and_price in sizes_and_prices:
                            qty_addings += size_and_price.qty
                    else:
                        qty_addings += flavor.qty

            for adding in addings:
                flavors = adding.flavors.all()
                for flavor in flavors:
                    sizes_and_prices = flavor.sizes_and_prices.all()
                    if not sizes_and_prices:
                        if request.POST["submit"] == f"inc-{adding.adding.id}-{flavor.flavor.id}":
                            if qty_addings < max_addings:
                                qty_addings += 1
                                flavor.qty += 1
                                flavor.save()
                        if request.POST["submit"] == f"dec-{adding.adding.id}-{flavor.flavor.id}":
                            if flavor.qty > 0:
                                qty_addings -= 1
                                flavor.qty -= 1
                                flavor.save()
                    else:
                        for size_and_price in sizes_and_prices:
                            if request.POST["submit"] == f"inc-{adding.adding.id}-{flavor.flavor.id}-{size_and_price.size_and_price.id}":
                                if qty_addings < max_addings:
                                    qty_addings += 1
                                    size_and_price.qty += 1
                                    size_and_price.save()
                            if request.POST["submit"] == f"dec-{adding.adding.id}-{flavor.flavor.id}-{size_and_price.size_and_price.id}":
                                if size_and_price.qty > 0:
                                    qty_addings -= 1
                                    size_and_price.qty -= 1
                                    size_and_price.save()

    ordering = get_ordering(order_item)

    ordering["total"] = 0
    order = Order.objects.filter(user=request.user).first()
    order_items = OrderItem.objects.filter(order=order).all()
    for item in order_items:
        item_ordering = get_ordering(item)
        subtotal = get_subtotal(item_ordering)
        ordering["total"] += subtotal
           
    ordering["subtotal"] = get_subtotal(ordering)

    context = {
        "dish": ordering["dish"],
        "type": ordering["type"],
        "flavor": ordering["flavor"],
        "min_addings": ordering["min_addings"],
        "max_addings": ordering["max_addings"],
        "addings": ordering["addings"],
        "subtotal": ordering["subtotal"],
        "total": ordering["total"]
    }
    return render(request, "orders/ordering.html", context)


def get_subtotal(ordering):
    subtotal = 0
    if ordering["flavor"]["size_and_price"]:
        subtotal = ordering["flavor"]["qty"] * ordering["flavor"]["size_and_price"].price

    for adding in ordering["addings"]:
        for flavor in adding["flavors"]:
            for size_and_price in flavor["sizes_and_prices"]:
                subtotal += size_and_price["qty"] * size_and_price["self"].price

    return subtotal


def get_order_item(user, flavor_id, size_id):
    order = Order.objects.filter(user=user).first()
    if not order:
        order = create_order(user)

    flavor = TypeFlavor.objects.filter(pk=flavor_id).first()
    size = Size.objects.filter(pk=size_id).first()

    order_item = OrderItem.objects.filter(order=order, flavor=flavor, size=size).first()
    if not order_item:
        order_item = create_order_item(order=order, flavor=flavor, size=size)
    return order_item


def create_order(user):
    order = Order(user=user)
    order.save()
    return order


def create_order_item(order, flavor, size):
    order_item = OrderItem(order=order, flavor=flavor, size=size)
    order_item.save()

    order_item.qty = 0

    type_ = flavor.super
    dish = type_.super
    dish_adding_table = DishAdding.objects
    dish_adding_flavor_table = AddingFlavor.objects
    addings_ids = ALL_ELEMENTS
    adding_flavors_ids = ALL_ELEMENTS
    adding_flavor_sizes_ids = ALL_ELEMENTS
    addings = get_view_types_or_addings(dish_adding_table, dish_adding_flavor_table, dish,
            addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    for adding in addings:
        order_item_adding = OrderItemAdding(adding=adding['self'])
        order_item_adding.save()

        for flavor in adding["flavors"]:
            order_item_adding_flavor = OrderItemAddingFlavor(flavor=flavor['self'], qty=0)
            order_item_adding_flavor.save()

            for size_and_price in flavor["sizes_and_prices"]:
                if size_and_price["self"]:
                    order_item_adding_flavor_size_and_price = OrderItemAddingFlavorSizeAndPrice(size_and_price=size_and_price["self"], qty=0)
                    order_item_adding_flavor_size_and_price.save()
                    order_item_adding_flavor.sizes_and_prices.add(order_item_adding_flavor_size_and_price)
                    order_item_adding_flavor.save()

            order_item_adding.flavors.add(order_item_adding_flavor)
            order_item_adding.save()

        order_item.addings.add(order_item_adding)
        order_item.save()

    order_item.save()
    return order_item


def get_ordering(order_item):
    flavor = order_item.flavor
    size = order_item.size

    ordering_flavor = {}
    ordering_flavor["self"] = flavor
    ordering_flavor["size_and_price"] = flavor.sizes_and_prices.filter(size=size).first()
    ordering_flavor["addings"] = flavor.addings.all()
    ordering_flavor["qty"] = order_item.qty

    type_ = flavor.super
    dish = type_.super
    ordering = {}
    ordering["type"] = type_
    ordering["dish"] = dish

    ordering["flavor"] = ordering_flavor

    if flavor.code < 0:
        ordering["min_addings"] = 0
        ordering["max_addings"] = -flavor.code
    else:
        ordering["min_addings"] = flavor.code
        ordering["max_addings"] = flavor.code

    dish_adding_table = DishAdding.objects
    dish_adding_flavor_table = AddingFlavor.objects
    addings_ids = ALL_ELEMENTS
    adding_flavors_ids = ALL_ELEMENTS
    adding_flavor_sizes_ids = ALL_ELEMENTS
    addings = get_view_types_or_addings(dish_adding_table, dish_adding_flavor_table, dish,
            addings_ids, adding_flavors_ids, adding_flavor_sizes_ids)

    ordering["addings"] = []
    addings_from_order = order_item.addings.all()
    ordering_adding = None
    for adding in addings:
        for adding_from_order in addings_from_order:
            if adding == adding_from_order.adding:
#            order_item_adding = OrderItemAdding.objects.filter(adding=adding['self']).first()
                ordering_adding = adding
                break
        if not ordering_adding:
            break

        adding_flavors = []
        adding_flavors_from_order = adding_from_order.flavors.all()
        ordering_adding_flavor = None
        for adding_flavor in adding["flavors"]:
            for adding_flavor_from_order in adding_flavors_from_order:
                if adding_flavor == adding_flavor_from_order.flavor:
#            order_item_adding_flavor = OrderItemAddingFlavor.objects.filter(flavor=flavor['self']).first()
#            ordering_adding_flavor = flavor
#            ordering_adding_flavor["qty"] = order_item_adding_flavor.qty
                    ordering_adding_flavor = flavor
                    ordering_adding_flavor["qty"] = adding_flavor_from_order.qty
                    break
            if not ordering_adding_flavor:
                break

        for adding_from_order in addings_from_order:
            if adding == adding_from_order.adding:
#            order_item_adding = OrderItemAdding.objects.filter(adding=adding['self']).first()
                ordering_adding = adding
                break
        if not ordering_adding:
            break

            sizes_and_prices = []
            for size_and_price in flavor["sizes_and_prices"]:
                ordering_adding_flavor_size_and_price = {
                    "self": size_and_price["self"],
                    "qty": None
                }

                if size_and_price["self"]:
                    order_item_adding_flavor_size_and_price = OrderItemAddingFlavorSizeAndPrice.objects.filter(size_and_price=size_and_price["self"]).first()
                    ordering_adding_flavor_size_and_price["qty"] = order_item_adding_flavor_size_and_price.qty

                sizes_and_prices.append(ordering_adding_flavor_size_and_price)

            ordering_adding_flavor["sizes_and_prices"] = sizes_and_prices
            flavors.append(ordering_adding_flavor)

        ordering_adding["flavors"] = flavors
        ordering["addings"].append(ordering_adding)

    return ordering


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
            element = table.filter(pk=id).first()
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

    type_or_adding_sizes = []

    all_sizes = Size.objects.all().order_by("sort_number")
    for size in all_sizes:
        found = False
        for flavor in flavors:
            flavor_sizes_and_prices = get_flavor_sizes_and_prices(flavor, flavor_sizes_ids)
            for flavor_size_and_price in flavor_sizes_and_prices:
                if size == flavor_size_and_price.size:
                    type_or_adding_sizes.append(size)
                    found = True
                    break
            if found:
                break

    return type_or_adding_sizes


def get_flavor_sizes_and_prices(flavor, flavor_sizes_ids):
    flavor_sizes_and_prices = []

    if flavor_sizes_ids is ALL_ELEMENTS:
        flavor_sizes_and_prices = flavor.sizes_and_prices.all()
    else:
        for flavor_size_id in flavor_sizes_ids:
            size_and_price = flavor.sizes_and_prices.filter(size__id == flavor_size_id)
            flavor_sizes_and_prices.append(size_and_price)

    return flavor_sizes_and_prices


def get_view_flavors(flavors, flavor_sizes_ids, type_or_adding_sizes):
    view_flavors = []

    for flavor in flavors:
        view_flavor = {}
        view_flavor["self"] = flavor

        view_flavor["addings"] = []
        if hasattr(flavor, "addings"):
            view_flavor["addings"] = flavor.addings.all().order_by("sort_number")

        view_flavor["sizes_and_prices"] = []
        for type_or_adding_size in type_or_adding_sizes:
            view_flavor_size_and_price = {
                "size": type_or_adding_size,
                "self": None
            }

            flavor_sizes_and_prices = get_flavor_sizes_and_prices(flavor, flavor_sizes_ids)
            for flavor_size_and_price in flavor_sizes_and_prices:
                if type_or_adding_size == flavor_size_and_price.size:
                    view_flavor_size_and_price["self"] = flavor_size_and_price
                    break
            view_flavor["sizes_and_prices"].append(view_flavor_size_and_price)

        view_flavors.append(view_flavor)

    return view_flavors


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

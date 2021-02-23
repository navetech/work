from django.contrib import admin

from .models import Dish, Adding
from .models import Size
from .models import Topping, SpecialPizza, PizzaType, PizzaFlavor, Pizza
from .models import SubFlavor, Sub, ExtraFlavor, Extra
from .models import PastaFlavor, Pasta
from .models import SaladFlavor, Salad
from .models import DinnerPlatterFlavor, DinnerPlatter
from .models import OrderStatus, Order
from .models import PizzaOrder, SubOrder, PastaOrder, SaladOrder, DinnerPlatterOrder

# Register your models here.
admin.site.register(Dish)
admin.site.register(Adding)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(SpecialPizza)
admin.site.register(PizzaType)
admin.site.register(PizzaFlavor)
admin.site.register(Pizza)
admin.site.register(SubFlavor)
admin.site.register(Sub)
admin.site.register(ExtraFlavor)
admin.site.register(Extra)
admin.site.register(PastaFlavor)
admin.site.register(Pasta)
admin.site.register(SaladFlavor)
admin.site.register(Salad)
admin.site.register(DinnerPlatterFlavor)
admin.site.register(DinnerPlatter)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(PizzaOrder)
admin.site.register(SubOrder)
admin.site.register(PastaOrder)
admin.site.register(SaladOrder)
admin.site.register(DinnerPlatterOrder)

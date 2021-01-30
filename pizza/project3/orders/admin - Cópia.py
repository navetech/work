from django.contrib import admin

from .models import Order
#from .models import Size, Order

from .models import Topping, SpecialPizza, Pizza, PizzaOrder
from .models import Sub, Extra, SubOrder
from .models import Pasta, PastaOrder, Salad, SaladOrder, DinnerPlatter, DinnerPlatterOrder

# Register your models here.
#admin.site.register(Size)
admin.site.register(Order)
admin.site.register(Topping)
admin.site.register(SpecialPizza)
#admin.site.register(PizzaType)
#admin.site.register(PizzaFlavor)
admin.site.register(Pizza)
admin.site.register(PizzaOrder)
admin.site.register(Sub)
admin.site.register(Extra)
admin.site.register(SubOrder)
admin.site.register(Pasta)
admin.site.register(PastaOrder)
admin.site.register(Salad)
admin.site.register(SaladOrder)
admin.site.register(DinnerPlatter)
admin.site.register(DinnerPlatterOrder)

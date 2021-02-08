from django.contrib import admin

from .models import Size
from .models import Topping, SpecialPizza, PizzaType, PizzaFlavor, Pizza
from .models import SubFlavor, Sub, ExtraFlavor, Extra
from .models import PastaFlavor, Pasta
from .models import SaladFlavor, Salad
from .models import DinnerPlatterFlavor, DinnerPlatter

# Register your models here.
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

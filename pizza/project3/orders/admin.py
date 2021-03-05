from django.contrib import admin


from .models import Size, SizeAndPrice
from .models import Dish, DishAdding, DishType
from .models import AddingFlavor, TypeFlavor
from .models import OrderStatus, Order, DishOrder

# Register your models here.
admin.site.register(Size)
admin.site.register(SizeAndPrice)
admin.site.register(Dish)
admin.site.register(DishAdding)
admin.site.register(DishType)
admin.site.register(AddingFlavor)
admin.site.register(TypeFlavor)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(DishOrder)

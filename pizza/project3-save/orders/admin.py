from django.contrib import admin


from .models import Size, SizeAndPrice
from .models import Dish, DishAdding, DishType
from .models import AddingFlavor, TypeFlavor

from .models import OrderStatus, Order
from .models import OrderItemAddingFlavorSizeAndPrice, OrderItemAddingFlavor
from .models import OrderItemAdding, OrderItem


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
admin.site.register(OrderItemAddingFlavorSizeAndPrice)
admin.site.register(OrderItemAddingFlavor)
admin.site.register(OrderItemAdding)
admin.site.register(OrderItem)

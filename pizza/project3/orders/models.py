from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class CommonInfo(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64, blank=True,)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.sort_number}, {self.name}"


class Size(CommonInfo):
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.code}"


class SizeAndPrice(models.Model):
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.CASCADE, related_name="size_sizesandprices")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.size}, {self.price}"


class Dish(CommonInfo):
    pass

    def __str__(self):
        return f"{CommonInfo.__str__(self)}"


class DishTypeOrAdding(CommonInfo):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_dishtypesoraddings")

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.dish}"


class TypeOrAddingFlavor(CommonInfo):
    type_or_adding = models.ForeignKey(DishTypeOrAdding, blank=True, on_delete=models.CASCADE, related_name="typeoradding_typeoraddingflavors")
    img = models.ImageField(upload_to='orders/static/orders/images/flavors/', default=None, blank=True)
    code = models.IntegerField(default= 0, blank=True)
    sizes_and_prices = models.ManyToManyField(SizeAndPrice, blank=True, related_name="sizesandprices_typeoraddingflavors")

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.type_or_adding}, {self.img}, {self.code}, {self.sizes_and_prices}"

    
class Plate(models.Model):
    flavor = models.ForeignKey(TypeOrAddingFlavor, on_delete=models.CASCADE, related_name="flavor_plates")
    addings = models.ManyToManyField(TypeOrAddingFlavor, blank=True, related_name="addings_plates")

    def __str__(self):
        return f"{self.flavor}, {self.addings}"


class OrderStatus(CommonInfo):
    pass


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_orders")

    def __str__(self):
        return f"{self.user}, {self.status}"


class PlateOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_plateorders")
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE, related_name="plate_plateorders")
    addings = models.ManyToManyField(TypeOrAddingFlavor, blank=True, related_name="addings_plateorders")

    def __str__(self):
        return f"{self.order}, {self.food}, {self.addings}"

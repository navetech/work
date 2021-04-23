from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class CommonInfo(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.sort_number}, {self.name}"


class Size(CommonInfo):
    code = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.code}"


class SizeAndPrice(models.Model):
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name="size_sizesandprices")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.size}, {self.price}"


class Dish(CommonInfo):
    pass


class TypeOrAddingCommonInfo(CommonInfo):
    super = models.ForeignKey(Dish, verbose_name="dish", on_delete=models.CASCADE,
        related_name="dish_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.super}"


class DishType(TypeOrAddingCommonInfo):
    pass


class DishAdding(TypeOrAddingCommonInfo):
    pass


class FlavorCommonInfo(CommonInfo):
    img = models.ImageField(upload_to='orders/static/orders/images/flavors/', default=None, blank=True)
    code = models.IntegerField(default= 0, blank=True)
    sizes_and_prices = models.ManyToManyField(SizeAndPrice, blank=True,
        related_name="sizesandprices_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.img}, {self.code}, {self.sizes_and_prices}"


class AddingFlavor(FlavorCommonInfo):
    super = models.ForeignKey(DishAdding, verbose_name="adding", on_delete=models.CASCADE, related_name="adding_addingflavors")

    def __str__(self):
        return f"{FlavorCommonInfo.__str__(self)}, {self.super}"


class TypeFlavor(FlavorCommonInfo):
    super = models.ForeignKey(DishType, verbose_name="type", on_delete=models.CASCADE, related_name="type_typeflavors")
    addings = models.ManyToManyField(AddingFlavor, blank=True, related_name="addings_typeflavors")

    def __str__(self):
        return f"{FlavorCommonInfo.__str__(self)}, {self.super}, {self.addings}"


class OrderStatus(CommonInfo):
    pass


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
#    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_orders")

    def __str__(self):
        return f"{self.user}, {self.status}"


class OrderItemAddingFlavorSizeAndPrice(models.Model):
    size_and_price = models.ForeignKey(SizeAndPrice, on_delete=models.CASCADE,
        related_name="sizeandprice_orderitemaddingflavorsizesandprices")
    qty = models.IntegerField(default= 0, blank=True)

    def __str__(self):
        return f"{self.size_and_price}, {self.qty}"


class OrderItemAddingFlavor(models.Model):
    flavor = models.ForeignKey(AddingFlavor, on_delete=models.CASCADE, related_name="flavor_orderitemaddingflavors")
    qty = models.IntegerField(default= 0, blank=True)
    sizes_and_prices = models.ManyToManyField(OrderItemAddingFlavorSizeAndPrice, blank=True,
        related_name="sizesandprices_orderitemaddingflavors")

    def __str__(self):
        return f"{self.flavor}, {self.qty}, {self.sizes_and_prices}"


class OrderItemAdding(models.Model):
    adding = models.ForeignKey(DishAdding, on_delete=models.CASCADE, related_name="adding_orderitemaddings")
    flavors = models.ManyToManyField(OrderItemAddingFlavor, blank=True, related_name="flavors_orderitemaddings")

    def __str__(self):
        return f"{self.adding}, {self.flavors}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_orderitems")
    flavor = models.ForeignKey(TypeFlavor, on_delete=models.CASCADE, related_name="flavor_orderitems")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_orderitems")
    qty = models.IntegerField(default= 1, blank=True)
    addings = models.ManyToManyField(OrderItemAdding, blank=True, related_name="addings_orderitems")

    def __str__(self):
        return f"{self.order}, {self.flavor}, {self.size}, {self.qty}, {self.addings}"

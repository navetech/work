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


class HistoryCommonInfo(CommonInfo):
    class Meta:
        abstract = True

    def __str__(self):
        return f"{CommonInfo.__str__(self)}"


class SizeCommonInfo(CommonInfo):
    code = models.CharField(max_length=2, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.code}"


class Size(SizeCommonInfo):
    def __str__(self):
        return f"{SizeCommonInfo.__str__(self)}"


class HistorySize(SizeCommonInfo):
    def __str__(self):
        return f"{SizeCommonInfo.__str__(self)}"


class SizeAndPriceCommonInfo(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.price}"


class SizeAndPrice(SizeAndPriceCommonInfo):
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name="size_sizesandprices")

    def __str__(self):
        return f"{self.size}, {SizeAndPriceCommonInfo.__str__(self)}"


class HistorySizeAndPrice(SizeAndPriceCommonInfo):
    size = models.ForeignKey(HistorySize, blank=True, null=True, on_delete=models.CASCADE,
        related_name="size_historysizesandprices")

    def __str__(self):
        return f"{self.size}, {SizeAndPriceCommonInfo.__str__(self)}"


class Dish(CommonInfo):
    pass


class HistoryDish(HistoryCommonInfo):
    pass


class TypeOrAddingCommonInfo(CommonInfo):
    super = models.ForeignKey(Dish, verbose_name="dish", on_delete=models.CASCADE,
        related_name="dish_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.super}"


class HistoryTypeOrAddingCommonInfo(HistoryCommonInfo):
    super = models.ForeignKey(HistoryDish, verbose_name="dish", on_delete=models.CASCADE,
        related_name="dish_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{HistoryCommonInfo.__str__(self)}, {self.super}"


class DishType(TypeOrAddingCommonInfo):
    pass


class HistoryDishType(HistoryTypeOrAddingCommonInfo):
    pass


class DishAdding(TypeOrAddingCommonInfo):
    pass


class HistoryDishAdding(HistoryTypeOrAddingCommonInfo):
    pass


class FlavorCommonCommonInfo(CommonInfo):
    img = models.ImageField(upload_to='orders/static/orders/images/flavors/', default=None, blank=True)
    code = models.IntegerField(default= 0, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{CommonInfo.__str__(self)}, {self.img}, {self.code}"


class FlavorCommonInfo(FlavorCommonCommonInfo):
    sizes_and_prices = models.ManyToManyField(SizeAndPrice, blank=True,
        related_name="sizesandprices_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{FlavorCommonCommonInfo.__str__(self)}, {self.sizes_and_prices}"


class HistoryFlavorCommonInfo(FlavorCommonCommonInfo):
    sizes_and_prices = models.ManyToManyField(HistorySizeAndPrice, blank=True,
        related_name="sizesandprices_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{FlavorCommonCommonInfo.__str__(self)}, {self.sizes_and_prices}"


class AddingFlavor(FlavorCommonInfo):
    super = models.ForeignKey(DishAdding, verbose_name="adding", on_delete=models.CASCADE, related_name="adding_addingflavors")

    def __str__(self):
        return f"{FlavorCommonInfo.__str__(self)}, {self.super}"


class HistoryAddingFlavor(HistoryFlavorCommonInfo):
    super = models.ForeignKey(HistoryDishAdding, verbose_name="adding", on_delete=models.CASCADE,
        related_name="adding_historyaddingflavors")

    def __str__(self):
        return f"{HistoryFlavorCommonInfo.__str__(self)}, {self.super}"


class TypeFlavor(FlavorCommonInfo):
    super = models.ForeignKey(DishType, verbose_name="type", on_delete=models.CASCADE, related_name="type_typeflavors")
    addings = models.ManyToManyField(AddingFlavor, blank=True, related_name="addings_typeflavors")

    def __str__(self):
        return f"{FlavorCommonInfo.__str__(self)}, {self.super}, {self.addings}"


class HistoryTypeFlavor(HistoryFlavorCommonInfo):
    super = models.ForeignKey(HistoryDishType, verbose_name="type", on_delete=models.CASCADE, related_name="type_historytypeflavors")
    addings = models.ManyToManyField(HistoryAddingFlavor, blank=True, related_name="addings_historytypeflavors")

    def __str__(self):
        return f"{HistoryFlavorCommonInfo.__str__(self)}, {self.super}, {self.addings}"


class OrderCommonInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="user_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user}"


class OrderStatus(CommonInfo):
    pass


class HistoryOrderStatus(HistoryCommonInfo):
    pass


class Order(OrderCommonInfo):
#    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_orders")

    def __str__(self):
        return f"{OrderCommonInfo.__str__(self)}"
#        return f"{OrderCommonInfo.__str__(self)}, {self.status}"


class HistoryOrder(OrderCommonInfo):
#    status = models.ForeignKey(HistoryOrderStatus, on_delete=models.CASCADE, related_name="status_historyorders")

    def __str__(self):
        return f"{OrderCommonInfo.__str__(self)}"
#        return f"{OrderCommonInfo.__str__(self)}, {self.status}"


class Quantity(models.Model):
    qty = models.IntegerField(default= 0, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.qty}"


class OrderItemAddingFlavorSizeAndPrice(Quantity):
    size_and_price = models.ForeignKey(SizeAndPrice, on_delete=models.CASCADE,
        related_name="sizeandprice_orderitemaddingflavorsizesandprices")

    def __str__(self):
        return f"{self.size_and_price}, {Quantity.__str__(self)}"


class HistoryOrderItemAddingFlavorSizeAndPrice(Quantity):
    size_and_price = models.ForeignKey(HistorySizeAndPrice, on_delete=models.CASCADE,
        related_name="sizeandprice_historyorderitemaddingflavorsizesandprices")

    def __str__(self):
        return f"{self.size_and_price}, {Quantity.__str__(self)}"


class OrderItemAddingFlavor(Quantity):
    flavor = models.ForeignKey(AddingFlavor, on_delete=models.CASCADE, related_name="flavor_orderitemaddingflavors")
    sizes_and_prices = models.ManyToManyField(OrderItemAddingFlavorSizeAndPrice, blank=True,
        related_name="sizesandprices_orderitemaddingflavors")

    def __str__(self):
        return f"{self.flavor}, {Quantity.__str__(self)}, {self.sizes_and_prices}"


class HistoryOrderItemAddingFlavor(Quantity):
    flavor = models.ForeignKey(HistoryAddingFlavor, on_delete=models.CASCADE, related_name="flavor_historyorderitemaddingflavors")
    sizes_and_prices = models.ManyToManyField(HistoryOrderItemAddingFlavorSizeAndPrice, blank=True,
        related_name="sizesandprices_historyorderitemaddingflavors")

    def __str__(self):
        return f"{self.flavor}, {Quantity.__str__(self)}, {self.sizes_and_prices}"


class OrderItemAdding(models.Model):
    adding = models.ForeignKey(DishAdding, on_delete=models.CASCADE, related_name="adding_orderitemaddings")
    flavors = models.ManyToManyField(OrderItemAddingFlavor, blank=True, related_name="flavors_orderitemaddings")

    def __str__(self):
        return f"{self.adding}, {self.flavors}"


class HistoryOrderItemAdding(models.Model):
    adding = models.ForeignKey(HistoryDishAdding, on_delete=models.CASCADE, related_name="adding_historyorderitemaddings")
    flavors = models.ManyToManyField(HistoryOrderItemAddingFlavor, blank=True, related_name="flavors_historyorderitemaddings")

    def __str__(self):
        return f"{self.adding}, {self.flavors}"


class OrderItem(Quantity):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_orderitems")
    flavor = models.ForeignKey(TypeFlavor, on_delete=models.CASCADE, related_name="flavor_orderitems")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_orderitems")
    addings = models.ManyToManyField(OrderItemAdding, blank=True, related_name="addings_orderitems")

    def __str__(self):
        return f"{self.order}, {self.flavor}, {self.size}, {Quantity.__str__(self)}, {self.addings}"


class HistoryOrderItem(Quantity):
    order = models.ForeignKey(HistoryOrder, on_delete=models.CASCADE, related_name="order_historyorderitems")
    flavor = models.ForeignKey(HistoryTypeFlavor, on_delete=models.CASCADE, related_name="flavor_historyorderitems")
    size = models.ForeignKey(HistorySize, on_delete=models.CASCADE, related_name="size_historyorderitems")
    addings = models.ManyToManyField(HistoryOrderItemAdding, blank=True, related_name="addings_historyorderitems")

    def __str__(self):
        return f"{self.order}, {self.flavor}, {self.size}, {Quantity.__str__(self)}, {self.addings}"

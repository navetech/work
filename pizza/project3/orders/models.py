from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class CommonInfo(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.sort_number} - {self.name}"


class Dish(CommonInfo):
    pass

    def __str__(self):
        return f"{CommonInfo.__str__(self)}"


class Adding(CommonInfo):
    pass

    def __str__(self):
        return f"{CommonInfo.__str__(self)}"


class Size(CommonInfo):
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{CommonInfo.__str__(self)} - {self.code}"


class PriceCommonInfo(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.price}"


class SizePriceCommonInfo(PriceCommonInfo):
    size = models.ForeignKey(Size, on_delete=models.CASCADE,
        related_name="size_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.size} - {PriceCommonInfo.__str__(self)}"


class Image(models.Model):
    src = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.src}"


class FlavorCommonInfo(CommonInfo):
    img = models.ForeignKey(Image, on_delete=models.CASCADE,
        related_name="size_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.img} - {CommonInfo.__str__(self)}"


class Topping(FlavorCommonInfo):
    pass


class SpecialPizza(CommonInfo):
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings_specialpizzas")

    def __str__(self):
        return f"{CommonInfo.__str__(self)} - {self.toppings}"


class PizzaType(CommonInfo):
    pass
        

class PizzaFlavor(FlavorCommonInfo):
    code = models.IntegerField(default=0)

    def __str__(self):
        return f"{CommonInfo.__str__(self)} - {self.code}"
        

class Pizza(SizePriceCommonInfo):
    type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name="type_pizzas")
    flavor = models.ForeignKey(PizzaFlavor, on_delete=models.CASCADE, related_name="flavor_pizzas")

    def __str__(self):
        return f"type: {self.type}, flavor: {self.flavor}, {SizePriceCommonInfo.__str__(self)}"


class SubFlavor(FlavorCommonInfo):
    pass
        

class Sub(SizePriceCommonInfo):
    flavor = models.ForeignKey(SubFlavor, on_delete=models.CASCADE, related_name="flavor_subs")

    def __str__(self):
        return f"flavor: {self.flavor}, {SizePriceCommonInfo.__str__(self)}"


class ExtraFlavor(FlavorCommonInfo):
    pass
        

class Extra(PriceCommonInfo):
    flavor = models.ForeignKey(ExtraFlavor, on_delete=models.CASCADE, related_name="flavor_extras")

    def __str__(self):
        return f"flavor: {self.flavor}, {PriceCommonInfo.__str__(self)}"


class PastaFlavor(FlavorCommonInfo):
    pass
        

class Pasta(PriceCommonInfo):
    flavor = models.ForeignKey(PastaFlavor, on_delete=models.CASCADE, related_name="flavor_pastas")

    def __str__(self):
        return f"flavor: {self.flavor}, {PriceCommonInfo.__str__(self)}"


class SaladFlavor(FlavorCommonInfo):
    pass
        

class Salad(PriceCommonInfo):
    flavor = models.ForeignKey(SaladFlavor, on_delete=models.CASCADE, related_name="flavor_salads")

    def __str__(self):
        return f"flavor: {self.flavor}, {PriceCommonInfo.__str__(self)}"


class DinnerPlatterFlavor(FlavorCommonInfo):
    pass
        

class DinnerPlatter(SizePriceCommonInfo):
    flavor = models.ForeignKey(DinnerPlatterFlavor, on_delete=models.CASCADE,
        related_name="flavor_dinnerplatters")

    def __str__(self):
        return f"flavor: {self.flavor}, {SizePriceCommonInfo.__str__(self)}"


class OrderStatus(CommonInfo):
    pass


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_orders")

    def __str__(self):
        return f"{self.order_user} - {self.order_status}"


class DishOrderCommonInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
        related_name="order_%(app_label)s_%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.order}"


class PizzaOrder(DishOrderCommonInfo):
    dish = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza_pizzaorders")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings_pizzaorders")


    def __str__(self):
        return f"pizza: {self.dish}, toppings: {self.toppings}"


class SubOrder(DishOrderCommonInfo):
    dish = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sub_suborders")
    extras = models.ManyToManyField(Extra, blank=True, related_name="extras_suborders")

    def __str__(self):
        return f"sub: {self.dish}, extra: {self.extras}"


class PastaOrder(DishOrderCommonInfo):
    dish = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="pasta_pastaorders")

    def __str__(self):
        return f"pasta: {self.dish}"


class SaladOrder(DishOrderCommonInfo):
    dish = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="salad_saladorders")

    def __str__(self):
        return f"salad: {self.dish}"


class DinnerPlatterOrder(DishOrderCommonInfo):
    dish = models.ForeignKey(DinnerPlatter, on_delete=models.CASCADE, related_name="dinnerplatter_dinnerplatterorders")

    def __str__(self):
        return f"dinner platter: {self.dish}"

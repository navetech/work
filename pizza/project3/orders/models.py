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


class Size(CommonInfo):
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{CommonInfo.__str__(self)} - {self.code}"


class Topping(CommonInfo):
    pass


class SpecialPizza(CommonInfo):
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings_specialpizzas")

    def __str__(self):
        return f"{CommonInfo.__str__(self)} - {self.toppings}"


class PizzaType(CommonInfo):
    pass
        

class PizzaFlavor(CommonInfo):
    code = models.IntegerField(default=0)

    def __str__(self):
        return f"{CommonInfo.__str__(self)} - {self.code}"
        

class Pizza(models.Model):
    dish_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name="type_pizzas")
    flavor = models.ForeignKey(PizzaFlavor, on_delete=models.CASCADE, related_name="flavor_pizzas")
    dish_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_pizzas")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"type: {self.dish_type}, flavor: {self.flavor}, size: {self.dish_size}, price: {self.price}"


class SubFlavor(CommonInfo):
    pass
        

class Sub(models.Model):
    flavor = models.ForeignKey(SubFlavor, on_delete=models.CASCADE, related_name="flavor_subs")
    dish_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_subs")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, size: {self.dish_size}, price: {self.price}"


class ExtraFlavor(CommonInfo):
    pass
        

class Extra(models.Model):
    flavor = models.ForeignKey(ExtraFlavor, on_delete=models.CASCADE, related_name="flavor_extras")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, price: {self.price}"


class PastaFlavor(CommonInfo):
    pass
        

class Pasta(models.Model):
    flavor = models.ForeignKey(PastaFlavor, on_delete=models.CASCADE, related_name="flavor_pastas")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, price: {self.price}"


class SaladFlavor(CommonInfo):
    pass
        

class Salad(models.Model):
    flavor = models.ForeignKey(SaladFlavor, on_delete=models.CASCADE, related_name="flavor_salads")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, price: {self.price}"


class DinnerPlatterFlavor(CommonInfo):
    pass
        

class DinnerPlatter(models.Model):
    flavor = models.ForeignKey(DinnerPlatterFlavor, on_delete=models.CASCADE, related_name="flavor_dinnerplatters")
    dish_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_dinnerplatters")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, size: {self.dish_size}, price: {self.price}"


class OrderStatus(CommonInfo):
    pass


class Order(models.Model):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_orders")

    def __str__(self):
        return f"{self.order_user} - {self.order_status}"


class PizzaOrder(models.Model):
    dish = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza_pizzaorders")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings_pizzaorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_pizzaorders")


    def __str__(self):
        return f"pizza: {self.dish}, toppings: {self.toppings}"


class SubOrder(models.Model):
    dish = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sub_suborders")
    extras = models.ManyToManyField(Extra, blank=True, related_name="extras_suborders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_suborders")

    def __str__(self):
        return f"sub: {self.dish}, extra: {self.extras}"


class PastaOrder(models.Model):
    dish = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="pasta_pastaorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_pastaorders")

    def __str__(self):
        return f"pasta: {self.dish}"


class SaladOrder(models.Model):
    dish = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="salad_saladorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_saladorders")

    def __str__(self):
        return f"salad: {self.dish}"


class DinnerPlatterOrder(models.Model):
    dish = models.ForeignKey(DinnerPlatter, on_delete=models.CASCADE, related_name="dinnerplatter_dinnerplatterorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_dinnerplatterorders")

    def __str__(self):
        return f"dinner platter: {self.dish}"

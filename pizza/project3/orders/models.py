from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Size(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.sort_number} - {self.name} - {self.code}"


class Topping(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"


class SpecialPizza(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings_specialpizzas")

    def __str__(self):
        return f"{self.sort_number} - {self.name} - {self.toppings}"


class PizzaType(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"
        

class PizzaFlavor(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)
    code = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sort_number} - {self.name} - {self.code}"
        

class Pizza(models.Model):
    pizza_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name="type_pizzas")
    flavor = models.ForeignKey(PizzaFlavor, on_delete=models.CASCADE, related_name="flavor_pizzas")
    pizza_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_pizzas")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"type: {self.pizza_type}, flavor: {self.flavor}, size: {self.pizza_size}, price: {self.price}"


class SubFlavor(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"
        

class Sub(models.Model):
    flavor = models.ForeignKey(SubFlavor, on_delete=models.CASCADE, related_name="flavor_subs")
    sub_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_subs")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, size: {self.sub_size}, price: {self.price}"


class ExtraFlavor(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"
        

class Extra(models.Model):
    flavor = models.ForeignKey(ExtraFlavor, on_delete=models.CASCADE, related_name="flavor_extras")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, price: {self.price}"


class PastaFlavor(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"
        

class Pasta(models.Model):
    flavor = models.ForeignKey(PastaFlavor, on_delete=models.CASCADE, related_name="flavor_pastas")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, price: {self.price}"


class SaladFlavor(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"
        

class Salad(models.Model):
    flavor = models.ForeignKey(SaladFlavor, on_delete=models.CASCADE, related_name="flavor_salads")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, price: {self.price}"


class DinnerPlatterFlavor(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"
        

class DinnerPlatter(models.Model):
    flavor = models.ForeignKey(DinnerPlatterFlavor, on_delete=models.CASCADE, related_name="flavor_dinnerplatters")
    dinnerplatter_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_dinnerplatters")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"flavor: {self.flavor}, size: {self.dinnerplatter_size}, price: {self.price}"


class OrderStatus(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"


class Order(models.Model):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="status_orders")

    def __str__(self):
        return f"{self.order_user} - {self.order_status}"


class PizzaOrder(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza_pizzaorders")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings_pizzaorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_pizzaorders")


    def __str__(self):
        return f"pizza: {self.pizza}, toppings: {self.toppings}"


class SubOrder(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sub_suborders")
    extra = models.ForeignKey(Extra, on_delete=models.CASCADE, related_name="extra_suborders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_suborders")

    def __str__(self):
        return f"sub: {self.sub}, extra: {self.extra}"


class PastaOrder(models.Model):
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="pasta_pastaorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_pastaorders")

    def __str__(self):
        return f"pasta: {self.pasta}"


class SaladOrder(models.Model):
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="salad_saladorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_saladorders")

    def __str__(self):
        return f"salad: {self.salad}"


class DinnerPlatterOrder(models.Model):
    dinnerplatter = models.ForeignKey(DinnerPlatter, on_delete=models.CASCADE, related_name="dinnerplatter_dinnerplatterorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_dinnerplatterorders")

    def __str__(self):
        return f"dinner platter: {self.dinnerplatter}"

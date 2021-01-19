from django.db import models

# Create your models here.
class Topping(models.Model):
      name = models.CharField(max_length=64)

      def __str__(self):
          return f"{self.name}"


class SpecialPizza(models.Model):
    topping_1 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="specials_topping_1")
    topping_2 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="specials_topping_2")
    topping_3 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="specials_topping_3")
    topping_4 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="specials_topping_4")

    def __str__(self):
        return f"toppings: {self.topping_1}, {self.topping_2}, {self.topping_3}, {self.topping_4}"


class Pizza(models.Model):
    PIZZA_TYPES = [
        ('R', 'Regular'),
        ('S', 'Sicilian'),
    ]
    
    PIZZA_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )

    class NumberOfToppings(models.IntegerChoices):
        CHEESE = 0
        ONE_TOPPING = 1
        TWO_TOPPINGS = 2
        THREE_TOPPINGS = 3
        SPECIAL = -1

    pizza_type = models.CharField(max_length=1, choices=PIZZA_TYPES)
    pizza_size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    toppings = models.IntegerField(choices=NumberOfToppings.choices)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"type: {self.pizza_type}, size: {self.pizza_size}, toppings: {self.toppings}, price: {self.price}"


class PizzaOrder(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="orders")
    topping_1 = models.ForeignKey(Topping, blank=True, null=True, on_delete=models.SET_NULL, related_name="orders_topping_1")
    topping_2 = models.ForeignKey(Topping, blank=True, null=True, on_delete=models.SET_NULL, related_name="orders_topping_2")
    topping_3 = models.ForeignKey(Topping, blank=True, null=True, on_delete=models.SET_NULL, related_name="orders_topping_3")

    def __str__(self):
        p = f"pizza: {self.pizza}"
        nl = '\n'
        t = f"toppings: {self.topping_1}, {self.topping_2}, {self.topping_3}"
        return p + nl + t


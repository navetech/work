from django.db import models

# Create your models here.
MEAL_SIZES = (
    ('S', 'Small'),
    ('L', 'Large'),
)


class Order(models.Model):
    closed = models.BooleanField(default=False)

    def __str__(self):
        '''
        pi = f"pizzas: {self.order_pizzas}"
        su = f"subs: {self.order_subs}"
        pa = f"pastas: {self.order_pastas}"
        sa = f"salads: {self.order_salads}"
        dp = f"dinner_platters: {self.order_dinner_platters}"
        nl = "\n"
        return pi + nl + su + nl + pa + nl + sa + nl + dp
        '''
        return f"closed: {self.closed}"


class Topping(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sort_number} - {self.name}"


class SpecialPizza(models.Model):
    sort_number = models.FloatField(default=0)
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="special_pizzas")

    def __str__(self):
        return f"{self.sort_number} - {self.name} - {self.toppings}"


class Pizza(models.Model):
    PIZZA_TYPES = [
        ('R', 'Regular'),
        ('S', 'Sicilian'),
    ]

    class NumberOfToppings(models.IntegerChoices):
        CHEESE = 0
        ONE_TOPPING = 1
        TWO_TOPPINGS = 2
        THREE_TOPPINGS = 3
        SPECIAL = -1

    p_flavor = models.FloatField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class PizzaOrder(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza_orders")
    topping_1 = models.ForeignKey(Topping, blank=True, null=True, on_delete=models.SET_NULL, related_name="topping_1_pizza_orders")
    topping_2 = models.ForeignKey(Topping, blank=True, null=True, on_delete=models.SET_NULL, related_name="topping_2_pizza_orders")
    topping_3 = models.ForeignKey(Topping, blank=True, null=True, on_delete=models.SET_NULL, related_name="topping_3_pizza_orders")

    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL, related_name="order_pizzas")


    def __str__(self):
        p = f"pizza: {self.pizza}"
        nl = '\n'
        t = f"toppings: {self.topping_1}, {self.topping_2}, {self.topping_3}"
        return p + nl + t


class Sub(models.Model):
    name = models.CharField(max_length=64)
    sub_size = models.CharField(max_length=1, choices=MEAL_SIZES)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}, size: {self.sub_size}, price: {self.price}"


class Extra(models.Model):
    name = models.CharField(max_length=64)
    extra_size = models.CharField(max_length=1, choices=MEAL_SIZES)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}, size: {self.extra_size}, price: {self.price}"


class SubOrder(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sub_orders")
    extra = models.ForeignKey(Extra, blank=True, null=True, on_delete=models.SET_NULL, related_name="extra_sub_orders")

    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL, related_name="order_subs")

    def __str__(self):
        s = f"sub: {self.sub}"
        nl = '\n'
        e = f"extra: {self.extra}"
        return s + nl + e


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}, price: {self.price}"


class PastaOrder(models.Model):
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="pasta_orders")

    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL, related_name="order_pastas")

    def __str__(self):
        return f"pasta: {self.pasta}"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}, price: {self.price}"


class SaladOrder(models.Model):
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="salad_orders")

    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL, related_name="order_salads")

    def __str__(self):
        return f"salad: {self.salad}"


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    dinner_platter_size = models.CharField(max_length=1, choices=MEAL_SIZES)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}, size: {self.dinner_platter_size}, price: {self.price}"


class DinnerPlatterOrder(models.Model):
    dinner_platter = models.ForeignKey(DinnerPlatter, on_delete=models.CASCADE, related_name="dinner_platter_orders")

    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL, related_name="order_dinner_platters")

    def __str__(self):
        return f"dinner_platter: {self.dinner_platter}"

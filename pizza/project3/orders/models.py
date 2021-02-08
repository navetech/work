from django.db import models

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
    toppings = models.ManyToManyField(Topping, blank=True, related_name="special_pizzas")

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

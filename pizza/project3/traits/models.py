from django.db import models

# Create your models here.

from texts.models import Text
from quantities.models import Quantity


class Trait(models.Model):
    name = models.ForeignKey(Text, blank=True, null=True, on_delete=models.CASCADE,
        related_name="name_traits")
    quantity = models.ForeignKey(Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name="quantity_traits")

    texts = models.ManyToManyField(Text, blank=True, related_name="texts_traits")

    def __str__(self):
        return f"{self.name}, {self.quantity}, {self.texts}"


from django.db import models

# Create your models here.

from texts.models import Text
from quantities.models import Quantity


class Trait(models.Model):
    tag = models.ForeignKey(
        Text, blank=True, null=True, on_delete=models.CASCADE,
        related_name="tag_trait_related"
    )
    quantity = models.ForeignKey(
        Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name="quantity_trait_related"
    )
    alt_tags = models.ManyToManyField(
        Text, blank=True, related_name="altTags_trait_related"
    )

    def __str__(self):
        return f"{self.tag}, {self.quantity}, {self.alt_tags}"

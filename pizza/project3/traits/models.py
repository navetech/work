from django.db import models

# Create your models here.

from texts.models import Text
from quantities.models import Quantity


class Trait(models.Model):
    tag = models.ForeignKey(
        Text, blank=True, null=True, on_delete=models.CASCADE,
        related_name='tag_Trait_related'
    )
    quantity = models.ForeignKey(
        Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name='quantity_Trait_related'
    )
    alt_tags = models.ManyToManyField(
        Text, blank=True,
        related_name='alt_tags_Trait_related'
    )

    def __str__(self):
        ret = ''
        if self.tag:
            ret += self.tag.__str__()
        if self.quantity:
            ret += self.quantity.__str__()
#        if self.alt_tags:
#            ret += self.alt_tags

        return ret

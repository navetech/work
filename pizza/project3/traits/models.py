from django.db import models

# Create your models here.

from texts.models import TextSegment
from quantities.models import Quantity


class Trait(models.Model):
    """
    tag = models.ForeignKey(
        Text, blank=True, null=True, on_delete=models.CASCADE,
        related_name='tag_Trait_related'
    )
    """
    text_segments = models.ManyToManyField(
        TextSegment, blank=True,
        related_name='text_segments_Trait_related'
    )

    quantity = models.ForeignKey(
        Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name='quantity_Trait_related'
    )

    def __str__(self):
        ret = ''
        text = self.text_segments.order_by('phrase_sort_number')
        for segment in text:
            ret += segment.phrase.__str__() + ' '
        if self.quantity:
            ret += ', ' + self.quantity.__str__()
#        if self.alt_tags:
#            ret += self.alt_tags

        return ret

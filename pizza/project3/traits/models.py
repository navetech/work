from django.db import models

# Create your models here.

from texts.models import TextSegment
from texts.models import Phrase
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

    short_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='short_name_Trait_related'
    )

    long_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='long_name_Trait_related'
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
        if self.short_name:
            ret += ', ' + self.short_name.__str__()
        if self.long_name:
            ret += ', ' + self.long_name.__str__()
        if self.quantity:
            ret += ', ' + self.quantity.__str__()
#        if self.alt_tags:
#            ret += self.alt_tags

        return ret

    def to_dict(self, dict):
        dict['id'] = self.id

        dict['short_name'] = self.short_name
        dict['long_name'] = self.long_name
        dict['quantity'] = self.quantity

        return

        return ret

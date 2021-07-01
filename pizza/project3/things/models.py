from django.db import models

# Create your models here.

from traits.models import Trait


class Thing(models.Model):
    trait = models.ForeignKey(
        Trait, blank=True, null=True, on_delete=models.CASCADE,
        related_name='trait_Thing_related'
    )

    parents = models.ManyToManyField(
        'self', blank=True,
        related_name='parents_Thing_related'
    )

    basics = models.ManyToManyField(
        'self', blank=True,
        related_name='basics_Thing_related'
    )
    basics_min_count = models.IntegerField(default=0, blank=True)
    basics_max_count = models.IntegerField(default=0, blank=True)

    adds = models.ManyToManyField(
        'self', blank=True,
        related_name='adds_Thing_related'
    )
    adds_min_count = models.IntegerField(default=0, blank=True)
    adds_max_count = models.IntegerField(default=0, blank=True)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return (
            f'{self.trait}, {self.parents}'
        )


class PickedThing(models.Model):
    thing = models.ForeignKey(
        Thing, blank=True, null=True, on_delete=models.CASCADE,
        related_name='thing_PickedThing_related'
    )
    count = models.IntegerField(default=0, blank=True)

    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.thing}, {self.count}, {self.date_time}'

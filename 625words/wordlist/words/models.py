from django.db import models

# Create your models here.

from phrases.models import Meaning


class Thema(models.Model):
    name = models.CharField(max_length=64)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.name}, '
            f'{self.sort_number}'
        )


class Group(models.Model):
    base_word = models.ForeignKey(
        'Word', blank=True, null=True, on_delete=models.CASCADE,
        related_name='base_word_Group_related'
    )

    grouping_key = models.CharField(max_length=64)

    def __str__(self):
        return (
            f'{self.base_word}, '
            f'{self.grouping_key}'
        )


class Word(models.Model):
    meaning = models.ForeignKey(
        Meaning, blank=True, null=True, on_delete=models.CASCADE,
        related_name='meaning_Word_related'
    )

    group = models.ForeignKey(
        Group, blank=True, null=True, on_delete=models.CASCADE,
        related_name='group_Word_related'
    )

    thema = models.ForeignKey(
        Thema, blank=True, null=True, on_delete=models.CASCADE,
        related_name='thema_Word_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.meaning}, '
            f'{self.group}, '
            f'{self.thema}, '
            f'{self.sort_number}'
        )

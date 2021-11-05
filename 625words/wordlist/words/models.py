from django.db import models

# Create your models here.

from phrases.models import Meaning


class Thema(models.Model):
    name = models.CharField(max_length=128)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.name}'
        )


class Group(models.Model):
    base_word = models.ForeignKey(
        'Word', blank=True, null=True, on_delete=models.CASCADE,
        related_name='base_word_Group_related'
    )

    grouping_key = models.CharField(max_length=128)

    def __str__(self):
        return (
            f'{self.grouping_key}, '
            f'base word: '
            f'{self.base_word}'
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
            f'{self.sort_number}, '
            f'meaning: '
            f'{self.meaning}'
        )

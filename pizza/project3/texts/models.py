from django.db import models

# Create your models here.

from languages.models import Iso_639_LanguageCode


class Phrase(models.Model):
    words = models.CharField(max_length=256, blank=True)

    languages = models.ManyToManyField(
        Iso_639_LanguageCode, blank=True,
        related_name='languages_Phrase_related'
    )
    """
    elements = models.ManyToManyField(
        'self', blank=True,
        related_name='elements_Phrase_related'
    )
    """

    def __str__(self):
        return (
            f'{self.words}'
#            f', {self.languages}, {self.elements}'
        )


class TextSegment(models.Model):
    phrase = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='phrase_TextSegment_related'
    )
    phrase_sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return f'{self.phrase}, {self.phrase_sort_number}'

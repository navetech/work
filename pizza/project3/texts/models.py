from django.db import models

# Create your models here.

from languages.models import Iso_639_LanguageCode


class Text(models.Model):
    words = models.CharField(max_length=256, blank=True)
    language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name="language_text_related"
    )
    elements = models.ManyToManyField(
        'self', blank=True, related_name="elements_text_related"
    )

    def __str__(self):
        return f"{self.words}, {self.language}, {self.elements}"

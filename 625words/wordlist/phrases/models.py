from django.db import models

# Create your models here.

from languages.models import Iso_639_LanguageCode
from languages.models import TransliterationSystem

from images.models import Image

from sounds.models import Sound


class SpellingLanguage(models.Model):
    language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_SpellingLanguage_related'
    )

    system = models.ForeignKey(
        TransliterationSystem, blank=True, null=True, on_delete=models.CASCADE,
        related_name='system_SpellingLanguage_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'language: '
            f'{self.language} '
            f'system: '
            f'{self.system}'
        )


class Spelling(models.Model):
    text = models.TextField(blank=True)

    spelling_language = models.ForeignKey(
        SpellingLanguage, blank=True, null=True, on_delete=models.CASCADE,
        related_name='spelling_language_Spelling_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.text},  '
            f'spelling language: '
            f'{self.spelling_language}'
        )


class Pronunciation(models.Model):
    spellings = models.ManyToManyField(
        Spelling, blank=True,
        related_name='spellings_Pronunciation_related'
    )

    sound = models.ForeignKey(
        Sound, blank=True, null=True, on_delete=models.CASCADE,
        related_name='sound_Pronunciation_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        spellings = self.spellings.all().order_by('sort_number')
        spellings_texts = []
        for spelling in spellings:
            spellings_texts.append(spelling.text)

        return (
            f'{self.sort_number}, '
            f'spellings:  '
            f'{spellings_texts}, '
        )


class Meaning(models.Model):
    definition = models.TextField(blank=True)

    images = models.ManyToManyField(
        Image, blank=True,
        related_name='images_Meaning_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        images = self.images.all().order_by('sort_number')
        images_links = []
        for image in images:
            images_links.append(image.link)

        return (
            f'{self.definition}'
        )


class Phrase(models.Model):
    meaning = models.ForeignKey(
        Meaning, blank=True, null=True, on_delete=models.CASCADE,
        related_name='meaning_Phrase_related'
    )

    language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_Phrase_related'
    )

    pronunciation = models.ForeignKey(
        Pronunciation, blank=True, null=True, on_delete=models.CASCADE,
        related_name='pronunciation_Phrase_related'
    )

    spellings = models.ManyToManyField(
        Spelling, blank=True,
        related_name='spellings_Phrase_related'
    )

    synonym_sort_number = models.FloatField(default=0, blank=True)

    examples = models.ManyToManyField(
        'self', blank=True,
        related_name='examples_Phrase_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        spellings = self.spellings.all().order_by('sort_number')
        spellings_texts = []
        for spelling in spellings:
            spellings_texts.append(spelling.text)

        return (
            f'{self.sort_number}, '
            f'{self.meaning} '
            f'{self.language} '
            f'{self.pronunciation} '
            f'spellings: '
            f'{spellings_texts}, '
            f'synonym sort number: '
            f'{self.synonym_sort_number}'
        )

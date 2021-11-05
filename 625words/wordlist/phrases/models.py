from django.db import models

# Create your models here.

from images.models import Image

from languages.models import TranscriptionSystem

from sounds.models import Sound
from languages.models import PronunciationForm

from languages.models import TransliterationScript

from languages.models import Iso_639_LanguageCode


class Meaning(models.Model):
    definition = models.TextField(blank=True)

    images = models.ManyToManyField(
        Image, blank=True,
        related_name='images_Meaning_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        images = self.images.all().order_by('sort_number')
        images_names = []
        for image in images:
            images_names.append(image.link)

        return (
            f'{self.definition}'
        )


class Transcription(models.Model):
    text = models.TextField(blank=True)

    system = models.ForeignKey(
        TranscriptionSystem, blank=True, null=True, on_delete=models.CASCADE,
        related_name='system_Transcription_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.text},  '
            f'system: '
            f'{self.system}'
        )


class Pronunciation(models.Model):
    sound = models.ForeignKey(
        Sound, blank=True, null=True, on_delete=models.CASCADE,
        related_name='sound_Pronunciation_related'
    )

    form = models.ForeignKey(
        PronunciationForm, blank=True, null=True, on_delete=models.CASCADE,
        related_name='form_Pronunciation_related'
    )

    transcriptions = models.ManyToManyField(
        Transcription, blank=True,
        related_name='transcriptions_Pronunciation_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        transcriptions = self.transcriptions.all().order_by('sort_number')
        transcriptions_texts = []
        for transcription in transcriptions:
            transcriptions_texts.append(transcription.text)

        return (
            f'{self.sort_number}, '
            f'{self.form}, '
            f'transcriptions:  '
            f'{transcriptions_texts}, '
        )


class Spelling(models.Model):
    text = models.TextField(blank=True)

    script = models.ForeignKey(
        TransliterationScript, blank=True, null=True, on_delete=models.CASCADE,
        related_name='script_Spelling_related'
    )

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.text},  '
            f'script: '
            f'{self.script}'
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

    pronunciation_sort_number = models.FloatField(default=0, blank=True)

    examples = models.ManyToManyField(
        'self', blank=True,
        related_name='examples_Phrase_related'
    )

    example_sort_number = models.FloatField(default=0, blank=True)

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
        )

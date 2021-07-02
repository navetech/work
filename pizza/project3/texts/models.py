from django.db import models

# Create your models here.

from languages.models import Iso_639_LanguageCode


class PhraseSetting(models.Model):
    default_language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='default_language_PhraseSetting_related'
    )

    target_language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='target_language_PhraseSetting_related'
    )



class Phrase(models.Model):
    words = models.CharField(max_length=256, blank=True)

    languages = models.ManyToManyField(
        Iso_639_LanguageCode, blank=True,
        related_name='languages_Phrase_related'
    )

    translation_of = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,
        related_name='translation_of_Phrase_related'
    )

    def __str__(self):
        
        return self.words

        origins = self.languages.all().order_by('sort_number')

        if setting.target_language:
            target = setting.target_language
        elif setting.default_language:
            target = setting.default_language
        else:
            target = Iso_639_LanguageCode.objects.order_by('sort_number').first()

        translated_words = None
        for origin in origins:
            if target == origin:
                translated_words = self.words
                break

        if not translated_words and self.translation_of:
            phrases = Phrase.objects.all()
            for phrase in phrases:
                if phrase != self and target in phrase.languages.all():
                    if phrase.translation_of == self.translation_of:
                        translated_words = phrase.words
                        break
        
        return translated_words


    def translate(self):
        setting = PhraseSetting.objects.first()
        if setting.target_language:
            target = setting.target_language
        elif setting.default_language:
            target = setting.default_language
        else:
            target = Iso_639_LanguageCode.objects.order_by('sort_number').first()

        origins = self.languages.all().order_by('sort_number')

        for origin in origins:
            if target == origin:
                return self.words

        phrases = Phrase.objects.all()
        for phrase in phrases:
            if phrase != self and target in phrase.languages.all():
                if phrase.translation_of:
                    if (
                        phrase.translation_of == self or
                        phrase.translation_of == self.translation_of
                    ):
                        return phrase.words
        
        return self.words


class TextSegment(models.Model):
    phrase = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='phrase_TextSegment_related'
    )
    phrase_sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        phrase_translated = self.phrase.translate()

        return f'{phrase_translated}, {self.phrase_sort_number}'

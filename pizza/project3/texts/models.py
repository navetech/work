from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from languages.models import Iso_639_LanguageCode



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
#        return self.words
        return self.translate()


    def translate_to(self, language):
        origins = self.languages.all().order_by('sort_number')

        for origin in origins:
            if language == origin:
                return self.words

        phrases = Phrase.objects.all()
        for phrase in phrases:
            if phrase != self and phrase.translation_of:
                if (
                    phrase.translation_of == self or
                    phrase.translation_of == self.translation_of
                ):
                    if language in phrase.languages.all():
                        return phrase.words
        
        return self.words


    def translate(self):
        settings = TextSetting.objects.first()
        if settings:
            if settings.user_language:
                language = settings.user_language.code
            elif settings.admin_language:
                language = settings.admin_language
            else:
                language = Iso_639_LanguageCode.objects.order_by('sort_number').first()
        else:
            language = Iso_639_LanguageCode.objects.order_by('sort_number').first()

        return self.translate_to(language)


class Language(models.Model):
    code = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='code_Language_related'
    )

    name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='name_Language_related'
    )

    def __str__(self):
        return (
            f'{self.code}, '
            f'{self.name}, '
        )


class TextSetting(models.Model):
    admin_language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='admin_language_TextSetting_related'
    )

    user_language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_language_TextSetting_related'
    )


    def __str__(self):
        return f'{self.target_language}'

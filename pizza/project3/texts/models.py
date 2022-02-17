from django.db import models

# Create your models here.

from languages.models import Iso_639_LanguageCode


def to_dict(object, **settings):
    if object:
        dict = object.to_dict(**settings)
    else:
        dict = {}

    return dict


def to_dict_list(manager, *order_by_field_names, **settings):
    dict_list = []

    if manager:
        objects = manager.all().order_by(*order_by_field_names)
        for object in objects:
            dict = to_dict(object, **settings)
            if dict:
                dict_list.append(dict)

    return dict_list


class Phrase(models.Model):
    words = models.TextField(blank=True)

    languages = models.ManyToManyField(
        Iso_639_LanguageCode, blank=True,
        related_name='languages_Phrase_related'
    )

    translation_of = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,
        related_name='translation_of_Phrase_related'
    )

    def __str__(self):
        languages = self.languages.all().order_by('sort_number')
        languages_names = []
        for language in languages:
            languages_names.append(language.english_name)

        return (
            f'{self.words} '
            # f'in '
            # f'{languages_names}, '
            # f'translation of '
            # f'{self.translation_of}'
        )

    def translate_to(self, language):
        origin_languages = self.languages.all().order_by('sort_number')

        if origin_languages and len(origin_languages) > 0:
            origin_language = origin_languages[0].english_name
        else:
            origin_language = None

        translated = {
            'words': self.words,
            'language': origin_language,
        }

        if not language:
            return translated
        else:
            for origin_language in origin_languages:
                if language.code == origin_language:
                    return translated

        translations = set(self.translation_of_Phrase_related.all())
        if self.translation_of:
            translations.add(self.translation_of)
        for translation in translations:
            if language.code in translation.languages.all():
                translated = {
                    'words': translation.words,
                    'language': language.code.english_name,
                }
                return translated
        return translated

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['words'] = self.words

        dict['languages'] = []
        languages = self.languages.all().order_by('sort_number')
        for language in languages:
            dict['languages'].append(language.english_name)

        dict['translation_of'] = to_dict(self.translation_of, **settings)

        if settings and settings['language']:
            language = settings['language']
        else:
            language = None

        dict['translated'] = self.translate_to(language)

        return dict

    def translate(self):
        language = Setting.get_first_language()

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
            f'{self.name}, '
            f'{self.code}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        if self.code:
            dict['code'] = self.code.english_name
        else:
            dict['code'] = {}

        dict['name'] = to_dict(self.name, **settings)

        return dict


class Setting(models.Model):
    language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_Setting_related'
    )

    def __str__(self):
        return (
            f'{self.language}'
        )

    @classmethod
    def get_first_language(cls):
        settings = cls.objects.first()
        if not settings:
            language = Language.objects.first()

            if language:
                settings = cls(language=language)
                settings.save()
        else:
            if not settings.language:
                language = Language.objects.first()

                if language:
                    settings.language = language
                    settings.save()
            else:
                language = settings.language

        return language

import csv

from first625words.models import Pronunciation
from first625words.models import Theme
from first625words.models import Language
from first625words.models import TransliterationSystem
from first625words.models import PronunciationSpelling

from . import helpers

from . import phrases

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import PHRASES_FILE_NAME_ROOT

from .settings import PRONUNCIATIONS_FILE_NAME_ROOT
from .settings import PRONUNCIATION_BASE_WORD_COLUMN
from .settings import PRONUNCIATION_BASE_WORD_HEADER
from .settings import PRONUNCIATION_GROUPING_COLUMN
from .settings import PRONUNCIATION_GROUPING_HEADER
from .settings import PRONUNCIATION_GROUPING_KEY_COLUMN
from .settings import PRONUNCIATION_GROUPING_KEY_HEADER
from .settings import PRONUNCIATION_SPELLING_COLUMN
from .settings import PRONUNCIATION_SPELLING_HEADER
from .settings import PRONUNCIATION_SOUND_COLUMN
from .settings import PRONUNCIATION_SOUND_HEADER
from .settings import PRONUNCIATION_PRONUNC_SPELL_COLUMN
from .settings import PRONUNCIATION_PRONUNC_SPELL_HEADER
from .settings import PRONUNCIATION_PRONUNC_SPELL_LANG_COLUMN
from .settings import PRONUNCIATION_PRONUNC_SPELL_LANG_HEADER


def clear_data_all():
    d = Pronunciation.objects.all()
    d.delete()


def import_data_for_words(path=None):
    print()

    themes_ = Theme.objects.all()

    for theme in themes_:
        import_data_for_words_by_theme(theme=theme, path=path)


def import_data_for_words_by_theme(theme, path=None):
    languages_ = Language.objects.all()

    for language in languages_:
        import_data_for_words_by_theme_and_language(
            theme=theme, language=language, path=path
            )


def import_data_for_words_by_theme_and_language(theme, language, path=None):
    file_exists = False
    data_valid_in_file = False
    data_inserted = False
    data_updated = False

    base_name = PRONUNCIATIONS_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += language.name.lower().replace(' ', '-')
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += PHRASES_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += theme.name.lower().replace(' ', '-')
    base_name += DATA_FILES_EXTENSION

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        database_modified = data_inserted or data_updated
        helpers.print_report(
            file_name=base_name, file_exists=file_exists,
            data_valid_in_file=data_valid_in_file,
            database_modified=database_modified
            )

        return

    file_exists = True

    phrase_prev = None

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            sound = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_SOUND_COLUMN,
                column_header=PRONUNCIATION_SOUND_HEADER
            )

            if sound is None:
                phrase_prev = None
                continue

            spell = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_PRONUNC_SPELL_COLUMN,
                column_header=PRONUNCIATION_PRONUNC_SPELL_HEADER
            )

            if spell is None:
                phrase_prev = None
                continue

            spell_lang = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_PRONUNC_SPELL_LANG_COLUMN,
                column_header=PRONUNCIATION_PRONUNC_SPELL_LANG_HEADER
            )

            if spell_lang is None:
                phrase_prev = None
                continue

            str_sound = str(sound)
            str_spell = str(spell)
            str_spell_lang = str(spell_lang)

            if (
                (not str_sound or str_sound.isspace())
                and
                (not str_spell or str_spell.isspace())
                and
                (not str_spell_lang or str_spell_lang.isspace())
            ):
                phrase_prev = None
                continue

            if (
                (
                    (str_spell and not str_spell.isspace())
                    and
                    (not str_spell_lang or str_spell_lang.isspace())
                )
                or
                (
                    (str_spell_lang and not str_spell_lang.isspace())
                    and
                    (not str_spell or str_spell.isspace())
                )
            ):
                phrase_prev = None
                continue

            column = {
                'base_word': PRONUNCIATION_BASE_WORD_COLUMN,
                'grouping': PRONUNCIATION_GROUPING_COLUMN,
                'grouping_key': PRONUNCIATION_GROUPING_KEY_COLUMN,
                'spelling': PRONUNCIATION_SPELLING_COLUMN
            }

            column_header = {
                'base_word': PRONUNCIATION_BASE_WORD_HEADER,
                'grouping': PRONUNCIATION_GROUPING_HEADER,
                'grouping_key': PRONUNCIATION_GROUPING_KEY_HEADER,
                'spelling': PRONUNCIATION_SPELLING_HEADER
            }

            from_row = phrases.get_data_from_row(
                row=row,
                column=column, column_header=column_header,
                theme=theme, data_prev=phrase_prev
                )

            if not from_row or not from_row['data']:
                continue

            phrase = from_row['data']

            phrase_prev = phrase

            data_valid_in_file = True

            spelling_language = None
            if str_spell_lang and not str_spell_lang.isspace():
                spelling_language = TransliterationSystem.objects.filter(
                    name=spell_lang
                    ).first()

                if not spelling_language:
                    spelling_language = TransliterationSystem(name=spell_lang)
                    spelling_language.save()

                    data_inserted = True

            spelling = None
            if str_spell and not str_spell.isspace():
                spelling = PronunciationSpelling.objects.filter(
                    text=spell, system=spelling_language
                    ).first()

                if not spelling:
                    spelling = PronunciationSpelling(
                        text=spell, system=spelling_language
                        )
                    spelling.save()

                    data_inserted = True

            if sound:
                if spelling:
                    pronunciation = Pronunciation.objects.filter(
                        sound=sound, spelling=spelling
                        ).first()

                    if not pronunciation:
                        pronunciation = Pronunciation(
                            sound=sound, spelling=spelling
                            )
                        pronunciation.save()

                        data_inserted = True
                else:
                    pronunciation = Pronunciation.objects.filter(
                        sound=sound
                        ).first()

                    if not pronunciation:
                        pronunciation = Pronunciation(sound=sound)
                        pronunciation.save()

                        data_inserted = True
            elif spelling:
                pronunciation = Pronunciation.objects.filter(
                    spelling=spelling
                    ).first()

                if not pronunciation:
                    pronunciation = Pronunciation(spelling=spelling)
                    pronunciation.save()

                    data_inserted = True
            else:
                pronunciation = None

            pronunciations_ = phrase.pronunciations.all()
            if pronunciation not in pronunciations_:
                phrase.pronunciations.add(pronunciation)

                data_updated = True

            database_modified = data_inserted or data_updated
            if (database_modified):
                print(
                    phrase.word.base_word.text, phrase.word.grouping,
                    phrase.word.grouping_key, phrase.spelling.text,
                    sound, spell, spell_lang
                    )
                print()

    database_modified = data_inserted or data_updated
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )


import csv

from first625words.models import Spelling
from first625words.models import Theme
from first625words.models import Language
from first625words.models import Phrase

from . import helpers

from . import words

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import WORDS_FILE_NAME_ROOT

from .settings import SPELLINGS_FILE_NAME_ROOT
from .settings import SPELLING_BASE_WORD_COLUMN
from .settings import SPELLING_BASE_WORD_HEADER
from .settings import SPELLING_GROUPING_COLUMN
from .settings import SPELLING_GROUPING_HEADER
from .settings import SPELLING_GROUPING_KEY_COLUMN
from .settings import SPELLING_GROUPING_KEY_HEADER
from .settings import SPELLING_COLUMN
from .settings import SPELLING_HEADER

"""
from .settings import SPELLINGS_FILE_NAME_ROOT
from .settings import PRONUNCIATIONS_FILE_NAME_ROOT
from .settings import PRONUNCIATION_SPELLING_COLUMN
from .settings import PRONUNCIATION_SPELLING_HEADER
from .settings import PRONUNCIATION_SOUND_COLUMN
from .settings import PRONUNCIATION_SOUND_HEADER
from .settings import PRONUNCIATION_PRONUNC_SPELL_COLUMN
from .settings import PRONUNCIATION_PRONUNC_SPELL_HEADER
from .settings import PRONUNCIATION_PRONUNC_SPELL_LANG_COLUMN
from .settings import PRONUNCIATION_PRONUNC_SPELL_LANG_HEADER
"""


def clear_data_all():
    d = Spelling.objects.all()
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

    base_name = SPELLINGS_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += language.name.lower().replace(' ', '-')
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += WORDS_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += theme.name.lower().replace(' ', '-')
    base_name += DATA_FILES_EXTENSION

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        database_modified = data_inserted
        helpers.print_report(
            file_name=base_name, file_exists=file_exists,
            data_valid_in_file=data_valid_in_file,
            database_modified=database_modified
            )

        return

    file_exists = True

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            spelling_text = helpers.get_cell_from_row(
                row=row, column=SPELLING_COLUMN, column_header=SPELLING_HEADER
            )

            if (
                spelling_text is None or
                not str(spelling_text) or str(spelling_text).isspace()
            ):
                continue

            column = {
                'base_word': SPELLING_BASE_WORD_COLUMN,
                'grouping': SPELLING_GROUPING_COLUMN,
                'grouping_key': SPELLING_GROUPING_KEY_COLUMN
            }

            column_header = {
                'base_word': SPELLING_BASE_WORD_HEADER,
                'grouping': SPELLING_GROUPING_HEADER,
                'grouping_key': SPELLING_GROUPING_KEY_HEADER
            }

            from_row = words.get_data_from_row(
                row=row, column=column,
                column_header=column_header, theme=theme
                )

            if not from_row or not from_row['data']:
                continue

            word = from_row['data']
            
            data_inserted = data_inserted or from_row['data_inserted']

            data_valid_in_file = True

            spelling = Spelling.objects.filter(text=spelling_text).first()
            if not spelling:
                spelling = Spelling(text=spelling_text)
                spelling.save()

                data_inserted = True

            phrase = Phrase.objects.filter(
                word=word,
                spelling=spelling,
                language=language
                ).first()

            if not phrase:
                phrase = Phrase(word=word, spelling=spelling, language=language)
                phrase.save()

                data_inserted = True

            database_modified = data_inserted
            if (database_modified):
                print(
                    word.base_word.text, word.grouping, word.grouping_key,
                    spelling.text
                    )
                print()

    database_modified = data_inserted
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )

"""
def clear_pronunciations_by_theme_and_language(theme, language):
    base_words_ = base_words.get_data(theme=theme)

    for base_word in base_words_:
        words_ = words.get_data(base_word=base_word)

        for word in words_:
            phrases_ = phrases.get_data(word=word)

            for phrase in phrases_:
                spelling = phrase.spelling
                if spelling and spelling.language == language:
                    pronunciations_ = spelling.pronunciations.all()

                    for pronunciation in pronunciations_:
                        spelling.pronunciations.remove(pronunciation)
                        pronunciation.delete()

                alt_spellings = phrase.alt_spellings.all()
                for spelling in alt_spellings:
                    if spelling and spelling.language == language:
                        pronunciations_ = spelling.pronunciations.all()

                        for pronunciation in pronunciations_:
                            spelling.pronunciations.remove(pronunciation)
                            pronunciation.delete()


def import_pronunciations(path=None):
    print()

    themes_ = themes.get_data_all()

    for theme in themes_:
        import_pronunciations_by_theme(theme=theme, path=path)


def import_pronunciations_by_theme(theme, path=None):
    print()

    languages_ = languages.get_data_all()

    for language in languages_:
        import_pronunciations_by_theme_and_language(
            theme=theme, language=language, path=path
            )


def import_pronunciations_by_theme_and_language(theme, language, path=None):
    base_name = f'{theme.name.lower()}'
    base_name += f'-{SPELLINGS_FILE_NAME_ROOT}'
    base_name += f'-{language.name.lower()}'
    base_name += f'-{PRONUNCIATIONS_FILE_NAME_ROOT}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_pronunciations_by_theme_and_language(theme=theme, language=language)

    spelling_prev = None

    print()

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            spelling_text = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_SPELLING_COLUMN,
                column_header=PRONUNCIATION_SPELLING_HEADER
            )

            if spelling_text is None:
                spelling_prev = None
                continue

            pronunc_sound = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_SOUND_COLUMN,
                column_header=PRONUNCIATION_SOUND_HEADER
            )

            if pronunc_sound is None:
                spelling_prev = None
                continue

            pronunc_spell_text = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_PRONUNC_SPELL_COLUMN,
                column_header=PRONUNCIATION_PRONUNC_SPELL_HEADER
            )

            if pronunc_spell_text is None:
                spelling_prev = None
                continue

            pronunc_spell_lang_name = helpers.get_cell_from_row(
                row=row, column=PRONUNCIATION_PRONUNC_SPELL_LANG_COLUMN,
                column_header=PRONUNCIATION_PRONUNC_SPELL_LANG_HEADER
            )

            if pronunc_spell_lang_name is None:
                spelling_prev = None
                continue

            str_pronunc_sound = str(pronunc_sound)
            str_pronunc_spell_text = str(pronunc_spell_text)
            str_pronunc_spell_lang_name = str(pronunc_spell_lang_name)

            if (
                (not str_pronunc_sound or str_pronunc_sound.isspace())
                and
                (
                    not str_pronunc_spell_text
                    or
                    str_pronunc_spell_text.isspace()
                )
                and
                (
                    not str_pronunc_spell_lang_name
                    or
                    str_pronunc_spell_lang_name.isspace()
                )
            ):
                spelling_prev = None
                continue

            if (
                (
                    (
                        str_pronunc_spell_text
                        and
                        not str_pronunc_spell_text.isspace()
                    )
                    and
                    (
                        not str_pronunc_spell_lang_name
                        or
                        str_pronunc_spell_lang_name.isspace()
                    )
                )
                or
                (
                    (
                        not str_pronunc_spell_text
                        or
                        str_pronunc_spell_text.isspace()
                    )
                    and
                    (
                        str_pronunc_spell_lang_name
                        and
                        not str_pronunc_spell_lang_name.isspace()
                    )
                )
            ):
                spelling_prev = None
                continue

            spelling = get_data(text=spelling_text, language=language).first()

            str_spelling_text = str(spelling_text)

            if not spelling:
                if (
                    spelling_prev
                    and
                    (not str_spelling_text or str_spelling_text.isspace())
                ):
                    spelling = spelling_prev
                else:
                    spelling = insert_data(
                        text=spelling_text, language=language
                        )

            spelling_prev = spelling

            pronunc_spell = None

            if (
                (
                    str_pronunc_spell_lang_name
                    and
                    not str_pronunc_spell_lang_name.isspace()
                )
                and
                (
                    str_pronunc_spell_text
                    and
                    not str_pronunc_spell_text.isspace()
                )
            ):
                pronunc_spell_lang = translit_systems.get_data(
                    name=pronunc_spell_lang_name
                    ).first()

                if not pronunc_spell_lang:
                    pronunc_spell_lang = translit_systems.insert_data(
                        name=pronunc_spell_lang_name
                        )

                pronunc_spell = pronunc_spellings.get_data(
                        text=pronunc_spell_text, system=pronunc_spell_lang
                        ).first()

                if not pronunc_spell:
                    pronunc_spell = pronunc_spellings.insert_data(
                            text=pronunc_spell_text,
                            system=pronunc_spell_lang
                            )

            pronunciation = pronunciations.get_data(
                sound=pronunc_sound, spelling=pronunc_spell
                ).first()

            if not pronunciation:
                pronunciation = pronunciations.insert_data(
                    sound=pronunc_sound, spelling=pronunc_spell
                    )

            pronunciations_ = spelling.pronunciations.all()
            if pronunciation not in pronunciations_:
                spelling.pronunciations.add(pronunciation)

            print()
            print(
                spelling.text, pronunciation.spelling.text,
                pronunciation.spelling.system.name,
                pronunciation.sound
                )

    print()
"""
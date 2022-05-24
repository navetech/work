import csv

from first625words.models import Spelling

from . import helpers

from . import themes
from . import base_words
from . import words
from . import languages
from . import translit_systems
from . import pronunc_spellings
from . import pronunciations
from . import phrases

from .settings import DATA_FILES_EXTENSION

from .settings import WORDS_SPELLINGS_FILE_NAME_ROOT
from .settings import SPELLING_BASE_WORD_COLUMN
from .settings import SPELLING_BASE_WORD_HEADER
from .settings import SPELLING_GROUPING_COLUMN
from .settings import SPELLING_GROUPING_HEADER
from .settings import SPELLING_GROUPING_KEY_COLUMN
from .settings import SPELLING_GROUPING_KEY_HEADER
from .settings import SPELLING_COLUMN
from .settings import SPELLING_HEADER
from .settings import SPELLING_ALT_COLUMN
from .settings import SPELLING_ALT_HEADER

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


def get_data_all():
    return Spelling.objects.all()


def get_data(text=None, language=None):
    if text is not None and str(text) and not str(text).isspace():
        if language:
            d = Spelling.objects.filter(
                text=text, language=language
                )
        else:
            d = Spelling.objects.filter(text=text)
    elif language:
        d = Spelling.objects.filter(language=language)
    else:
        d = None

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(text, language):
    d = Spelling(text=text, language=language)
    d.save()

    return d


def clear_data_for_words_by_theme_and_language(theme, language):
    base_words_ = base_words.get_data(theme=theme)

    for base_word in base_words_:
        words_ = words.get_data(base_word=base_word)

        for word in words_:
            phrases_ = phrases.get_data(word=word)

            for phrase in phrases_:
                spelling = phrase.spelling
                if spelling and spelling.language == language:
                    phrase.spelling = None
                    phrase.save()
                    spelling.delete()

                alt_spellings = phrase.alt_spellings.all()
                for spelling in alt_spellings:
                    if spelling and spelling.language == language:
                        phrase.alt_spellings.remove(spelling)
                        spelling.delete()


def import_data_for_words(path=None):
    print()

    themes_ = themes.get_data_all()

    for theme in themes_:
        import_data_for_words_by_theme(theme=theme, path=path)


def import_data_for_words_by_theme(theme, path=None):
    print()

    languages_ = languages.get_data_all()

    for language in languages_:
        import_data_for_words_by_theme_and_language(
            theme=theme, language=language, path=path
            )


def import_data_for_words_by_theme_and_language(theme, language, path=None):
    base_name = f'{theme.name.lower()}'
    base_name += f'-{WORDS_SPELLINGS_FILE_NAME_ROOT}'
    base_name += f'-{language.name.lower()}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_data_for_words_by_theme_and_language(theme=theme, language=language)

    word_prev = None
    spelling_prev = None

    print()

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            spelling_text = helpers.get_cell_from_row(
                row=row, column=SPELLING_COLUMN, column_header=SPELLING_HEADER
            )

            if spelling_text is None:
                word_prev = None
                spelling_prev = None
                continue

            alt_spelling_text = helpers.get_cell_from_row(
                row=row, column=SPELLING_ALT_COLUMN,
                column_header=SPELLING_ALT_HEADER
            )

            if alt_spelling_text is None:
                word_prev = None
                spelling_prev = None
                continue

            str_spelling_text = str(spelling_text)
            str_alt_spelling_text = str(alt_spelling_text)

            if (
                (not str_spelling_text or str_spelling_text.isspace())
                and
                (not str_alt_spelling_text or str_alt_spelling_text.isspace())
            ):
                word_prev = None
                spelling_prev = None
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

            word = words.get_data_from_row(
                row=row,
                column=column, column_header=column_header,
                theme=theme, word_prev=word_prev
                )

            word_prev = word

            if not word:
                spelling_prev = None
                continue

            spelling = get_data(text=spelling_text, language=language).first()

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

            phrase = phrases.get_data(word=word, spelling=spelling).first()
            if not phrase:
                phrase = phrases.insert_data(word=word, spelling=spelling)

            print()
            print(
                word.base_word.text, word.grouping, word.grouping_key,
                spelling.text, end=' '
                )

            if str_alt_spelling_text and not str_alt_spelling_text.isspace():
                alt_spelling = get_data(
                    text=alt_spelling_text, language=language
                    ).first()

                if not alt_spelling:
                    alt_spelling = insert_data(
                        text=alt_spelling_text, language=language
                        )

                alt_spellings = phrase.alt_spellings.all()
                if alt_spelling not in alt_spellings:
                    phrase.alt_spellings.add(alt_spelling)

                print(alt_spelling.text)

            print()

    print()


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

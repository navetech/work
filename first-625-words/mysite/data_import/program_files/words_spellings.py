import csv

from first625words.models import Spelling

from . import helpers

from . import themes
from . import base_words
from . import words
from . import languages
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


def get_data_all():
    return Spelling.objects.all()


def get_data(text, language):
    return Spelling.objects.filter(text=text, language=language)


def clear_data_all():
    d = get_data_all()
    d.delete()


def clear_data_by_theme_and_language(theme, language):
    base_words_ = base_words.get_data(theme=theme)

    for base_word in base_words_:
        words_ = words.get_data(base_word=base_word)

        for word in words_:
            phrases_ = phrases.get_data(word=word)

            for phrase in phrases_:
                spelling = phrase.spelling
                if spelling.language == language:
                    phrase.spelling = None
                    phrase.save()
                    spelling.delete()

                alt_spellings = phrase.alt_spellings.all()
                for spelling in alt_spellings:
                    if spelling.language == language:
                        phrase.alt_spellings.remove(spelling)
                        spelling.delete()


def insert_data(text, language):
    d = Spelling(text=text, language=language)
    d.save()

    return d


def import_data(path=None):
    print()

    themes_ = themes.get_data_all()

    for theme in themes_:
        import_data_by_theme(theme=theme, path=path)


def import_data_by_theme(theme, path=None):
    print()

    languages_ = languages.get_data_all()

    for language in languages_:
        import_data_by_theme_and_language(theme=theme, language=language, path=path)


def import_data_by_theme_and_language(theme, language, path=None):
    base_name = f'{theme.name.lower()}'
    base_name += f'-{WORDS_SPELLINGS_FILE_NAME_ROOT}'
    base_name += f'-{language.name.lower()}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_data_by_theme_and_language(theme=theme, language=language)

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
                continue

            alt_spelling_text = helpers.get_cell_from_row(
                row=row, column=SPELLING_ALT_COLUMN, column_header=SPELLING_ALT_HEADER
            )

            if alt_spelling_text is None:
                word_prev = None
                continue


            str_spelling_text = str(spelling_text)
            str_alt_spelling_text = str(alt_spelling_text)

            if (
                (not str_spelling_text or str_spelling_text.isspace())
                and
                (not str_alt_spelling_text or str_alt_spelling_text.isspace())
            ):
                word_prev = None
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
                    spelling = insert_data(spelling_text, language=language).first()
            
            spelling_prev = spelling

            phrase = phrases.get_data(word=word, spelling=spelling).first()
            if not phrase:
                phrase = phrases.insert_data(word=word, spelling=spelling)

            if str_alt_spelling_text and not str_alt_spelling_text.isspace():
                alt_spelling = get_data(text=alt_spelling_text, language=language).first()

                if not alt_spelling:
                    alt_spelling = insert_data(alt_spelling_text, language=language).first()

                alt_spellings = phrase.alt_spellings.all()
                if not alt_spelling in alt_spellings:
                    phrase.alt_spellings.add(alt_spelling)

            print()
            print(
                word.base_word.text, word.grouping, word.grouping_key,
                spelling.text, end=' '
                )
            if alt_spelling:
                print(alt_spelling.text)
            print()

    print()

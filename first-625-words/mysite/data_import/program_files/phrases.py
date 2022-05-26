import csv

from first625words.models import Phrase
from first625words.models import Theme
from first625words.models import Language
from first625words.models import Spelling

from . import helpers

from . import words

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import WORDS_FILE_NAME_ROOT

from .settings import PHRASES_FILE_NAME_ROOT
from .settings import PHRASE_BASE_WORD_COLUMN
from .settings import PHRASE_BASE_WORD_HEADER
from .settings import PHRASE_GROUPING_COLUMN
from .settings import PHRASE_GROUPING_HEADER
from .settings import PHRASE_GROUPING_KEY_COLUMN
from .settings import PHRASE_GROUPING_KEY_HEADER
from .settings import PHRASE_SPELLING_COLUMN
from .settings import PHRASE_SPELLING_HEADER


def clear_data_all():
    d = Phrase.objects.all()
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

    base_name = PHRASES_FILE_NAME_ROOT
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
                row=row, column=PHRASE_SPELLING_COLUMN, column_header=PHRASE_SPELLING_HEADER
            )

            if (
                spelling_text is None or
                not str(spelling_text) or str(spelling_text).isspace()
            ):
                continue

            column = {
                'base_word': PHRASE_BASE_WORD_COLUMN,
                'grouping': PHRASE_GROUPING_COLUMN,
                'grouping_key': PHRASE_GROUPING_KEY_COLUMN
            }

            column_header = {
                'base_word': PHRASE_BASE_WORD_HEADER,
                'grouping': PHRASE_GROUPING_HEADER,
                'grouping_key': PHRASE_GROUPING_KEY_HEADER
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

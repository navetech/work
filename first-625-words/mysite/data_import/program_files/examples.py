import csv

from first625words.models import Example

from first625words.models import Theme
from first625words.models import Language

from . import helpers

from . import phrases

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import PHRASES_FILE_NAME_ROOT

from .settings import EXAMPLES_FILE_NAME_ROOT
from .settings import EXAMPLE_BASE_WORD_COLUMN
from .settings import EXAMPLE_BASE_WORD_HEADER
from .settings import EXAMPLE_GROUPING_COLUMN
from .settings import EXAMPLE_GROUPING_HEADER
from .settings import EXAMPLE_GROUPING_KEY_COLUMN
from .settings import EXAMPLE_GROUPING_KEY_HEADER
from .settings import EXAMPLE_SPELLING_COLUMN
from .settings import EXAMPLE_SPELLING_HEADER
from .settings import EXAMPLE_COLUMN
from .settings import EXAMPLE_HEADER
from .settings import EXAMPLE_CREDITS_COLUMN
from .settings import EXAMPLE_CREDITS_HEADER


def clear_data_all():
    d = Example.objects.all()
    d.delete()


def import_data_for_phrases(path=None):
    print()

    themes_ = Theme.objects.all()
    for theme in themes_:
        import_data_for_phrases_by_theme(theme=theme, path=path)


def import_data_for_phrases_by_theme(theme, path=None):
    languages_ = Language.objects.all()
    for language in languages_:
        import_data_for_phrases_by_theme_and_language(
            theme=theme, language=language, path=path
            )


def import_data_for_phrases_by_theme_and_language(theme, language, path=None):
    file_exists = False
    data_valid_in_file = False
    data_inserted = False
    data_updated = False

    base_name = EXAMPLES_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += PHRASES_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += language.name.lower().replace(' ', '-')
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

    with open(target_path, encoding="utf8") as file:
        rows = csv.reader(file)
        for row in rows:
            text = helpers.get_cell_from_row(
                row=row, column=EXAMPLE_COLUMN,
                column_header=EXAMPLE_HEADER
            )

            if text is None or not str(text) or str(text).isspace():
                phrase_prev = None
                continue

            credits = helpers.get_cell_from_row(
                row=row, column=EXAMPLE_CREDITS_COLUMN,
                column_header=EXAMPLE_CREDITS_HEADER
            )

            if credits is None:
                phrase_prev = None
                continue

            column = {
                'base_word': EXAMPLE_BASE_WORD_COLUMN,
                'grouping': EXAMPLE_GROUPING_COLUMN,
                'grouping_key': EXAMPLE_GROUPING_KEY_COLUMN,
                'spelling': EXAMPLE_SPELLING_COLUMN
            }

            column_header = {
                'base_word': EXAMPLE_BASE_WORD_HEADER,
                'grouping': EXAMPLE_GROUPING_HEADER,
                'grouping_key': EXAMPLE_GROUPING_KEY_HEADER,
                'spelling': EXAMPLE_SPELLING_HEADER
            }

            phrase = phrases.get_data_from_row(
                row=row,
                column=column, column_header=column_header,
                theme=theme, language=language, data_prev=phrase_prev
                )

            if not phrase:
                phrase_prev = None
                continue

            phrase_prev = phrase

            data_valid_in_file = True

            example = Example.objects.filter(
                text=text, credits=credits
                ).first()

            if not example:
                example = Example(
                    text=text, credits=credits
                    )
                example.save()
                data_inserted = True

            examples_ = phrase.examples.all()
            if example not in examples_:
                phrase.examples.add(example)
                data_updated = True

            database_modified = data_inserted or data_updated
            if database_modified:
                print(
                    phrase.word.base_word.text, phrase.word.grouping,
                    phrase.word.grouping_key, phrase.spelling.text,
                    example.text, example.credits
                    )
                print()

    database_modified = data_inserted or data_updated
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )

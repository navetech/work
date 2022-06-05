import csv

from first625words.models import Definition

from first625words.models import Theme
from first625words.models import Language

from . import helpers

from . import phrases

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import PHRASES_FILE_NAME_ROOT

from .settings import DEFINITIONS_FILE_NAME_ROOT
from .settings import DEFINITION_BASE_WORD_COLUMN
from .settings import DEFINITION_BASE_WORD_HEADER
from .settings import DEFINITION_GROUPING_COLUMN
from .settings import DEFINITION_GROUPING_HEADER
from .settings import DEFINITION_GROUPING_KEY_COLUMN
from .settings import DEFINITION_GROUPING_KEY_HEADER
from .settings import DEFINITION_SPELLING_COLUMN
from .settings import DEFINITION_SPELLING_HEADER
from .settings import DEFINITION_COLUMN
from .settings import DEFINITION_HEADER


def clear_data_all():
    d = Definition.objects.all()
    d.delete()


def import_data_for_phrases(path=None):
    print()

    themes_ = Theme.objects.all()
    for theme in themes_:
        import_data_for_phrases_by_theme(theme=theme, path=path)


def import_data_for_phrases_by_theme(theme, path=None):
    languages_ = Language.objects.all()
    for language in languages_:
        import_data_for_phrases_by_theme_and_lang(
            theme=theme, lang=language, path=path
            )


def import_data_for_phrases_by_theme_and_lang(theme, lang, path=None):
    languages_ = Language.objects.all()
    for language in languages_:
        import_data_for_phrases_by_theme_and_lang_and_def_lang(
            theme=theme, lang=lang, def_lang=language, path=path
            )


def import_data_for_phrases_by_theme_and_lang_and_def_lang(
        theme, lang, def_lang, path=None
        ):

    file_exists = False
    data_valid_in_file = False
    data_inserted = False
    data_updated = False

    base_name = DEFINITIONS_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += def_lang.name.lower().replace(' ', '-')
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += PHRASES_FILE_NAME_ROOT
    base_name += DATA_FILES_FILE_NAME_ROOTS_SEPARATOR
    base_name += lang.name.lower().replace(' ', '-')
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
                row=row, column=DEFINITION_COLUMN,
                column_header=DEFINITION_HEADER
            )

            if text is None or not str(text) or str(text).isspace():
                phrase_prev = None
                continue

            column = {
                'base_word': DEFINITION_BASE_WORD_COLUMN,
                'grouping': DEFINITION_GROUPING_COLUMN,
                'grouping_key': DEFINITION_GROUPING_KEY_COLUMN,
                'spelling': DEFINITION_SPELLING_COLUMN
            }

            column_header = {
                'base_word': DEFINITION_BASE_WORD_HEADER,
                'grouping': DEFINITION_GROUPING_HEADER,
                'grouping_key': DEFINITION_GROUPING_KEY_HEADER,
                'spelling': DEFINITION_SPELLING_HEADER
            }

            phrase = phrases.get_data_from_row(
                row=row,
                column=column, column_header=column_header,
                theme=theme, language=lang, data_prev=phrase_prev
                )

            if not phrase:
                phrase_prev = None
                continue

            phrase_prev = phrase

            data_valid_in_file = True

            definition = Definition.objects.filter(
                text=text, language=def_lang
                ).first()

            if not definition:
                definition = Definition(
                    text=text, language=def_lang
                    )
                definition.save()
                data_inserted = True

            definitions_ = phrase.definitions.all()
            if definition not in definitions_:
                phrase.definitions.add(definition)

                data_updated = True

            database_modified = data_inserted or data_updated
            if database_modified:
                print(
                    phrase.word.base_word.text, phrase.word.grouping,
                    phrase.word.grouping_key, phrase.spelling.text,
                    definition.text, definition.language
                    )
                print()

    database_modified = data_inserted or data_updated
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )

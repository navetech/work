import csv

from first625words.models import BaseWord
from first625words.models import Theme

from . import helpers

from .settings import SORT_NUMBER_DEFAULT
from .settings import SORT_NUMBER_INC_DEFAULT

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import BASE_WORDS_FILE_NAME_ROOT
from .settings import BASE_WORD_COLUMN
from .settings import BASE_WORD_HEADER

from .settings import BASE_WORDS_LIMIT_MAX_BY_THEME


def clear_data_all():
    d = BaseWord.objects.all()
    d.delete()


def import_data(path=None):
    print()

    themes_ = Theme.objects.all()

    for theme in themes_:
        import_data_by_theme(theme=theme, path=path)


def import_data_by_theme(theme, path=None):
    file_exists = False
    data_valid_in_file = False
    data_inserted = False

    base_name = BASE_WORDS_FILE_NAME_ROOT
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

        count = (
            theme.sort_number * BASE_WORDS_LIMIT_MAX_BY_THEME
         ) + SORT_NUMBER_DEFAULT

        for row in rows:
            text = helpers.get_cell_from_row(
                row=row, column=BASE_WORD_COLUMN,
                column_header=BASE_WORD_HEADER
            )

            if text is None or not str(text) or str(text).isspace():
                continue

            data_valid_in_file = True

            base_word = BaseWord.objects.filter(text=text, theme=theme).first()
            if not base_word:
                base_word = BaseWord(text=text, theme=theme, sort_number=count)
                base_word.save()

                data_inserted = True

            database_modified = data_inserted
            if (database_modified):
                print(base_word.text, base_word.theme.name, base_word.sort_number)
                print()

            count += SORT_NUMBER_INC_DEFAULT

    database_modified = data_inserted
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )


def get_data_from_row(
        row, column, column_header, theme, data_prev=None):

    text = helpers.get_cell_from_row(
        row=row, column=column, column_header=column_header
    )

    if text is None:
        return None

    if str(text) and not str(text).isspace():
        base_word = BaseWord.objects.filter(text=text, theme=theme).first()
    else:
        base_word_prev = data_prev
        base_word = base_word_prev

    return base_word

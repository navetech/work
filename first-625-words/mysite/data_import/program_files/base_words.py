import os
import csv

from first625words.models import BaseWord

from . import helpers

from . import themes

from .settings import SORT_NUMBER_DEFAULT
from .settings import SORT_NUMBER_INC_DEFAULT

from .settings import DATA_FILE_NAME_ENDING_BASE_WORDS
from .settings import BASE_WORD_TEXT_COLUMN
from .settings import BASE_WORD_TEXT_HEADER

from .settings import BASE_WORDS_LIMIT_MAX_BY_THEME


def get_data_all():
    return BaseWord.objects.all()


def get_data(text=None, theme=None):
    if text is None:
        if theme is None:
            d = None
        else:
            d = BaseWord.objects.filter(theme=theme)
    elif theme is None:
        d = BaseWord.objects.filter(text=text)
    else:
        d = BaseWord.objects.filter(text=text, theme=theme)

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def clear_data(text=None, theme=None):
    d = get_data(text=text, theme=theme)
    d.delete()


def insert_data(text, theme, sort_number):
    d = BaseWord(text=text, theme=theme, sort_number=sort_number)
    d.save()


def import_data(path=None):
    themes_ = themes.get_data_all()

    for theme in themes_:
        import_data_by_theme(theme=theme, path=path)


def import_data_by_theme(theme, path=None):
    target_path = build_target_path(theme=theme, path=path)
    if not os.path.isfile(target_path):
        return

    clear_data(theme=theme)

    with open(target_path) as file:
        rows = csv.reader(file)
        
        count = (
            theme.sort_number * BASE_WORDS_LIMIT_MAX_BY_THEME
         ) + SORT_NUMBER_DEFAULT

        for row in rows:
            text = row[BASE_WORD_TEXT_COLUMN]
            if not text:
                return

            if text == BASE_WORD_TEXT_HEADER:
                return

            print(text, theme.name, count)

            d = get_data(text=text, theme=theme)

            if not d:
                insert_data(text=text, theme=theme, sort_number=count)

            count += SORT_NUMBER_INC_DEFAULT


def build_target_path(theme, path):
    base_name = f'{theme.name.lower()}{DATA_FILE_NAME_ENDING_BASE_WORDS}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)

    return target_path


def get_data_from_row(
    row, row_column, column_header,
    theme=None, base_word_prev=None
    ):

    base_word_text = helpers.get_cell_data_from_row(
        row=row, row_column=row_column, column_header=column_header
        )

    if base_word_text:
        base_word = get_data(text=base_word_text, theme=theme).first()
    elif base_word_text is None:
        base_word = None
    else:
        base_word = base_word_prev

    return base_word

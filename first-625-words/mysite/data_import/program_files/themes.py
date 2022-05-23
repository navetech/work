import csv

from first625words.models import Theme

from . import helpers

from .settings import SORT_NUMBER_DEFAULT
from .settings import SORT_NUMBER_INC_DEFAULT

from .settings import THEMES_FILE_NAME
from .settings import THEME_COLUMN
from .settings import THEME_HEADER


def get_data_all():
    return Theme.objects.all()


def get_data(name):
    return Theme.objects.filter(name=name)


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(name, sort_number):
    d = Theme(name=name, sort_number=sort_number)
    d.save()

    return d


def import_data(path=None):
    base_name = THEMES_FILE_NAME

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_data_all()

    with open(target_path) as file:
        rows = csv.reader(file)

        count = SORT_NUMBER_DEFAULT
        
        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=THEME_COLUMN, column_header=THEME_HEADER
            )

            if not name:
                continue

            theme = get_data(name=name)
            if not theme:
                theme = insert_data(name=name, sort_number=count)

            print(theme.name, theme.sort_number)

            count += SORT_NUMBER_INC_DEFAULT

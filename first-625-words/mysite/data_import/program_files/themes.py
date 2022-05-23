import csv

from first625words.models import Theme

from . import helpers

from .settings import SORT_NUMBER_DEFAULT
from .settings import SORT_NUMBER_INC_DEFAULT

from .settings import DATA_FILES_EXTENSION

from .settings import THEMES_FILE_NAME_ROOT
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
    print()

    base_name = f'{THEMES_FILE_NAME_ROOT}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_data_all()

    print()

    with open(target_path) as file:
        rows = csv.reader(file)

        count = SORT_NUMBER_DEFAULT
        
        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=THEME_COLUMN, column_header=THEME_HEADER
            )

            if name is None or not str(name) or str(name).isspace():
                continue

            theme = get_data(name=name)
            if not theme:
                theme = insert_data(name=name, sort_number=count)

            print()
            print(theme.name, theme.sort_number)

            count += SORT_NUMBER_INC_DEFAULT

    print()

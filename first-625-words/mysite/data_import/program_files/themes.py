import csv

from first625words.models import Theme

from . import helpers

from .settings import DATA_FILES_EXTENSION

from .settings import THEMES_FILE_NAME_ROOT
from .settings import THEME_COLUMN
from .settings import THEME_HEADER
from .settings import THEME_SORT_NUMBER_COLUMN
from .settings import THEME_SORT_NUMBER_HEADER


def clear_data_all():
    d = Theme.objects.all()
    d.delete()


def import_data(path=None):
    print()

    file_exists = False
    data_valid_in_file = False
    data_inserted = False
    data_updated = False

    base_name = THEMES_FILE_NAME_ROOT
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

    with open(target_path, encoding="utf8") as file:
        rows = csv.reader(file)
        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=THEME_COLUMN, column_header=THEME_HEADER
            )

            if name is None or not str(name) or str(name).isspace():
                continue

            from_row = helpers.get_sort_number_from_row(
                row=row,
                column=THEME_SORT_NUMBER_COLUMN,
                column_header=THEME_SORT_NUMBER_HEADER,
                model=Theme
            )

            if not from_row:
                continue

            sort_number = from_row['sort_number']
            if sort_number is None:
                continue

            sort_number_cell = from_row['cell']

            data_valid_in_file = True

            theme = Theme.objects.filter(name=name).first()
            if not theme:
                theme = Theme(name=name, sort_number=sort_number)
                theme.save()
                data_inserted = True
            elif str(sort_number_cell) and not str(sort_number_cell).isspace():
                if theme.sort_number != sort_number:
                    theme.sort_number = sort_number
                    theme.save()
                    data_updated = True

            database_modified = data_inserted or data_updated
            if database_modified:
                print(theme.name, theme.sort_number)
                print()

    database_modified = data_inserted or data_updated
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )

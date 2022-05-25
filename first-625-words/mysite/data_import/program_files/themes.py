import csv

from first625words.models import Theme

from . import helpers

from .settings import SORT_NUMBER_DEFAULT
from .settings import SORT_NUMBER_INC_DEFAULT

from .settings import DATA_FILES_EXTENSION

from .settings import THEMES_FILE_NAME_ROOT
from .settings import THEME_COLUMN
from .settings import THEME_HEADER


def clear_data_all():
    d = Theme.objects.all()
    d.delete()


def import_data(path=None):
    print()

    file_exists = False
    data_valid_in_file = False
    data_inserted = False

    base_name = THEMES_FILE_NAME_ROOT
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

        count = SORT_NUMBER_DEFAULT

        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=THEME_COLUMN, column_header=THEME_HEADER
            )

            if name is None or not str(name) or str(name).isspace():
                continue

            data_valid_in_file = True

            theme = Theme.objects.filter(name=name).first()
            if not theme:
                theme = Theme(name=name, sort_number=count)
                theme.save()

                data_inserted = True

            database_modified = data_inserted
            if (database_modified):
                print(theme.name, theme.sort_number)
                print()

            count += SORT_NUMBER_INC_DEFAULT

    database_modified = data_inserted
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )

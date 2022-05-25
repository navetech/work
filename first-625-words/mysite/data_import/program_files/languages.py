import csv

from first625words.models import Language

from . import helpers

from .settings import DATA_FILES_EXTENSION

from .settings import LANGUAGES_FILE_NAME_ROOT
from .settings import LANGUAGE_COLUMN
from .settings import LANGUAGE_HEADER


def clear_data_all():
    d = Language.objects.all()
    d.delete()


def import_data(path=None):
    print()

    file_exists = False
    data_valid_in_file = False
    data_inserted = False

    base_name = f'{LANGUAGES_FILE_NAME_ROOT}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        database_modified = data_inserted
        helpers.print_report(
            file_name=base_name, file_exists=file_exists,
            data_valid_in_file=data_valid_in_file,
            database_modified=database_modified
            )
            
        print()

        return

    file_exists = True

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=LANGUAGE_COLUMN, column_header=LANGUAGE_HEADER
            )

            if name is None or not str(name) or str(name).isspace():
                continue

            data_valid_in_file = True

            language = Language.objects.filter(name=name).first()
            if not language:
                language = Language(name=name)
                language.save()

                data_inserted = True

            database_modified = data_inserted
            if (database_modified):
                print(language.name)
                print()

    database_modified = data_inserted
    helpers.print_report(
        file_name=base_name, file_exists=file_exists,
        data_valid_in_file=data_valid_in_file,
        database_modified=database_modified
        )
        
    print()

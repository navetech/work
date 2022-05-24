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

    base_name = f'{LANGUAGES_FILE_NAME_ROOT}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_data_all()

    print()

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=LANGUAGE_COLUMN, column_header=LANGUAGE_HEADER
            )

            if name is None or not str(name) or str(name).isspace():
                continue

            language = Language.objects.filter(name=name)
            if not language:
                language = Language(name=name)
                language.save()

            print()
            print(language.name)

    print()

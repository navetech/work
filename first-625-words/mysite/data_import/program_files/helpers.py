import os

from .settings import DATA_FILES_DIR

from .settings import FILE_EXISTS_NOT
from .settings import DATA_VALID_IN_FILE_NOT
from .settings import DATABASE_MODIFIED_FOR_FILE_NOT


def build_target_path(base_name, path=None):
    if path:
        target_path = os.path.join(path, base_name)
    else:
        target_dir = os.path.join(os.path.dirname(__file__), DATA_FILES_DIR)
        t_p = os.path.join(target_dir, base_name)
        target_path = os.path.normpath(t_p)

    if not os.path.isfile(target_path):
        return None

    return target_path


def get_cell_from_row(row, column, column_header=None):
    if len(row) <= column:
        return ''

    cell = row[column]
    if column_header is not None and cell == column_header:
        return None
    else:
        return cell


def print_report(file_name='', file_exists=True, data_valid_in_file=True, database_modified=True):
    if not file_exists:
        pass
        # print(f'{FILE_EXISTS_NOT}: {file_name}')
        # print()
    elif not data_valid_in_file:
        print(f'{DATA_VALID_IN_FILE_NOT}: {file_name}')
        print()
    elif not database_modified:
        print(f'{DATABASE_MODIFIED_FOR_FILE_NOT}: {file_name}')
        print()

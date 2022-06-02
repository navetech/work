import os

from .settings import FILE_EXISTS_NOT, SORT_NUMBER_DEFAULT, SORT_NUMBER_INC_DEFAULT
from .settings import DATA_VALID_IN_FILE_NOT
from .settings import DATABASE_MODIFIED_FOR_FILE_NOT

from .settings import DATA_FILES_DIR


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


def get_cell_from_row(row, column, column_header):
    if len(row) <= column:
        return ''

    cell = row[column]
    if cell == column_header:
        return None
    else:
        return cell


def get_sort_number_from_row(row, column, column_header, model):
    data = {}

    cell = get_cell_from_row(
        row=row, column=column, column_header=column_header
    )

    if cell is not None and (not str(cell) or str(cell).isspace()):
        d = model.objects.order_by("-sort_number")
        if d.count() < 1:
            sort_number = SORT_NUMBER_DEFAULT
        else:
            sort_number = d[0].sort_number + SORT_NUMBER_INC_DEFAULT
    else:
        sort_number = cell

    data['cell'] = cell
    data['sort_number'] = sort_number

    return data


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

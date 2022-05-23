import os

from .settings import DATA_FILES_DIR


def build_target_path(base_name, path=None):
    if path:
        target_path = os.path.join(path, base_name)
    else:
        target_dir = os.path.join(os.path.dirname(__file__), DATA_FILES_DIR)
        t_p = os.path.join(target_dir, base_name)
        target_path = os.path.normpath(t_p)

    if not os.path.isfile(target_path):
        # print(f'Is not a file: {target_path}')
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


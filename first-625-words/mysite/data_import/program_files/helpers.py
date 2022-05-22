import os

from .settings import DATA_FILES_DIR


def build_target_path(base_name, path):
    if path:
        target_path = os.path.join(path, base_name)
    else:
        target_dir = os.path.join(os.path.dirname(__file__), DATA_FILES_DIR)
        t_p = os.path.join(target_dir, base_name)
        target_path = os.path.normpath(t_p)

    return target_path


def get_cell_data_from_row(row, row_column, column_header):
    cell_data = row[row_column]

    if cell_data == column_header:
        cell_data = None

    return cell_data

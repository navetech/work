import os


def build_target_path(target_base_name, path):
    if path:
        target_path = os.path.join(path, target_base_name)
    else:
        target_dir_name = os.path.join(os.path.dirname(__file__), '../data_files')
        target_path = os.path.join(target_dir_name, target_base_name)
        target_path = os.path.normpath(target_path)

    return target_path

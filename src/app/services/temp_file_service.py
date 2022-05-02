import logging
import os.path

import glob

from app import TEMP_FOLDER_PATH


class FileMode:
    FILE_MODE_READ = "r"
    FILE_MODE_APPEND = "a"
    FILE_MODE_OVERWRITE = "w"
    FILE_MODE_CREATE_ERROR_IF_EXISTS = "x"


def get_temp_folder_path(filename=None) -> str:
    if not os.path.isdir(TEMP_FOLDER_PATH):
        os.mkdir(TEMP_FOLDER_PATH)

    if filename is None:
        return TEMP_FOLDER_PATH

    return os.path.join(TEMP_FOLDER_PATH, filename)


def check_if_temp_file_exists(filename: str) -> bool:
    file_path = get_temp_folder_path(filename=filename)

    return os.path.isfile(file_path)


def read_temp_file(filename: str, filemode: str = FileMode.FILE_MODE_READ) -> str:
    file_path = get_temp_folder_path(filename=filename)
    with open(file=file_path, mode=filemode) as file:
        content = file.read()

    return content


def clear_temp_folder():
    folder_path = get_temp_folder_path()
    logging.debug(f"Cleaning temp folder '({folder_path})'...")
    temp_files = glob.glob(os.path.join(folder_path, "*"))
    for temp_file in temp_files:
        logging.debug(f"Deleting temp file '{temp_file}'")
        os.remove(temp_file)


def save_temp_file(filename: str, content: str = "", filemode: str = FileMode.FILE_MODE_OVERWRITE) -> str:
    file_path = get_temp_folder_path(filename=filename)
    with open(file=file_path, mode=filemode) as file:
        file.write(content)

    return file_path


def remove_temp_file(filename: str):
    file_path = get_temp_folder_path(filename=filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

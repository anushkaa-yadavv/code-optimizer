import shutil
import os

def create_backup(file_path):
    base, ext = os.path.splitext(file_path)
    backup_path = base + "_backup" + ext
    shutil.copy(file_path, backup_path)
    return backup_path

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
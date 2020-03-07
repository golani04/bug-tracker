import os
from backend.config import project_path


def dbpath():
    print(project_path)
    return os.path.normpath(os.path.join(project_path, "db_files"))

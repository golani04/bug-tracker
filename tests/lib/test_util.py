import os
from backend.config import project_path
from backend.lib.util import dbpath


def test_path_to_db():
    folder_name = "db_files"
    assert os.path.join(project_path, folder_name) == dbpath()

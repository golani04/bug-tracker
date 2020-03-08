import os
from backend.config import project_path
from backend.lib.const import _DB_PATH, ISSUES_PATH, PROJECTS_PATH, USERS_PATH


def test_path_to_db():
    folder_name = "db_files"
    assert os.path.join(project_path, folder_name) == _DB_PATH


def test_path_to_issues():
    folder_name = "issues"
    assert os.path.join(_DB_PATH, folder_name) == ISSUES_PATH


def test_path_to_projects():
    folder_name = "projects"
    assert os.path.join(_DB_PATH, folder_name) == PROJECTS_PATH


def test_path_to_users():
    folder_name = "users"
    assert os.path.join(_DB_PATH, folder_name) == USERS_PATH

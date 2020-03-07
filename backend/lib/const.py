import os
from backend.config import project_path


_DB_PATH = os.path.normpath(os.path.join(project_path, "db_files"))
PROJECTS_PATH = os.path.normpath(os.path.join(_DB_PATH, "projects"))
ISSUES_PATH = os.path.normpath(os.path.join(_DB_PATH, "issues"))
USERS_PATH = os.path.normpath(os.path.join(_DB_PATH, "users"))

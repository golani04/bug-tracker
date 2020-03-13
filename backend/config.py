import os
from dotenv import load_dotenv


# load env variables
load_dotenv()
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
_db_path = os.path.normpath(os.path.join(project_path, "db_files"))


class db_config:
    ISSUES_PATH = os.path.normpath(os.path.join(_db_path, "issues", "issues.json"))
    PROJECTS_PATH = os.path.normpath(os.path.join(_db_path, "projects", "projects.json"))
    USERS_PATH = os.path.normpath(os.path.join(_db_path, "users", "users.json"))

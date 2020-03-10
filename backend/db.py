import json
from typing import Dict, List
from backend.lib.const import ISSUES_PATH, PROJECTS_PATH, USERS_PATH


_projects = PROJECTS_PATH
_issues = ISSUES_PATH
_users = USERS_PATH


def _read_json(path: str) -> List[Dict]:
    try:
        with open(path, mode="r") as f:
            return json.loads(f.read())
    except (IOError, FileExistsError, FileExistsError):
        return []


def _save_json(path: str, data: List) -> bool:
    try:
        with open(path, mode="w") as f:
            f.write(json.loads(data))
            return True
    except (IOError, FileExistsError, FileExistsError):
        return False


def get_projects() -> List[Dict]:
    return _read_json(_projects)


def save_projects(projects: List[Dict]) -> bool:
    return _save_json(_projects, projects)

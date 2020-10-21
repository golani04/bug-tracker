import json
from typing import Dict, List

from backend.config import settings


def _read_json(path: str) -> List[Dict]:
    try:
        settings.logger.info(f"Path to json: {path}")
        with open(path, mode="r") as f:
            return json.loads(f.read())
    except IOError:
        return []


def _save_json(path: str, data: List) -> bool:
    try:
        with open(path, mode="w") as f:
            f.write(json.dumps(data))
            return True
    except IOError:
        return False


class FileDatabase:
    @staticmethod
    def get_projects() -> List[Dict]:
        return _read_json(settings.projects_path)

    @staticmethod
    def save_projects(projects: List[Dict]) -> bool:
        return _save_json(settings.projects_path, projects)

    @staticmethod
    def get_issues() -> List[Dict]:
        return _read_json(settings.issues_path)

    @staticmethod
    def save_issues(issues: List[Dict]) -> bool:
        return _save_json(settings.issues_path, issues)

    @staticmethod
    def get_users() -> List[Dict]:
        return _read_json(settings.users_path)

    @staticmethod
    def save_users(users: List[Dict]) -> bool:
        return _save_json(settings.users_path, users)

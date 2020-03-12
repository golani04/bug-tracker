import json
from dataclasses import dataclass, field
from typing import Dict, List


def _read_json(path: str) -> List[Dict]:
    try:
        with open(path, mode="r") as f:
            return json.loads(f.read())
    except (IOError, FileExistsError, FileExistsError):
        return []


def _save_json(path: str, data: List) -> bool:
    try:
        with open(path, mode="w") as f:
            f.write(json.dumps(data))
            return True
    except (IOError, FileExistsError, FileExistsError):
        return False


@dataclass
class DB:
    config: object = field(default_factory=object)

    def get_projects(self) -> List[Dict]:
        return _read_json(self.config.PROJECTS_PATH)

    def save_projects(self, projects: List[Dict]) -> bool:
        return _save_json(self.config.PROJECTS_PATH, projects)

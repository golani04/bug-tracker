from backend.schemas.util import find_item_by_id
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from backend.db import FileDatabase
from backend.schemas.projects import Project


router = APIRouter()
db = FileDatabase()


@router.get("/", response_model=List[Project])
def get_projects():
    return db.get_projects()


@router.get("/{project_id}", response_model=Project)
def get_issue(project_id: UUID):
    project = find_item_by_id(db.get_projects(), project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Required project is missing"
        )

    return project

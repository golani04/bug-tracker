from backend.schemas.util import find_item_by_id
from backend.db import FileDatabase
from fastapi import APIRouter, status, HTTPException
from typing import List

from backend.schemas.issues import Issue, IssueCreate


router = APIRouter()
db = FileDatabase()


@router.get("/", response_model=List[Issue])
def get_issues():
    return db.get_issues()


@router.post("/", response_model=Issue, status_code=status.HTTP_201_CREATED)
def create_issue(data: IssueCreate):
    issue = IssueCreate(data)
    return issue


@router.get("/{issue_id}", response_model=Issue)
def get_issue(issue_id: int):
    issue = find_item_by_id(db.get_issues(), issue_id)
    if issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Required issue is missing"
        )

    return issue



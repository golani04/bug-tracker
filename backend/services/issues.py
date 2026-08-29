from pydantic import TypeAdapter

from backend.repositories.issues import IssueRepository
from backend.schemas.issues import Issue as IssueSchema, IssueArgs, IssueCreate, IssueUpdate


type_adapter = TypeAdapter(list[IssueSchema])


class IssueService:
    def __init__(self, repository: IssueRepository) -> None:
        self.repository = repository

    def get_issues(
        self, query_params: IssueArgs | None = None, project_id: int | None = None
    ) -> list[IssueSchema]:
        filters = query_params.model_dump(exclude_none=True) if query_params else {}
        if project_id is not None:
            filters["project_id"] = project_id

        self.repository.set_filters(filters)
        issues = self.repository.get_items()

        return type_adapter.validate_python(issues)

    def get_issue(self, issue_id: int, owner_id: int) -> IssueSchema:
        issue = self.repository.get_by_id(issue_id)
        if issue is None or issue.project.owner_id != owner_id:
            raise ValueError("Issue not found")

        return IssueSchema.model_validate(issue)

    def create_issue(self, issue: IssueCreate, reporter_id: int, project_id: int) -> int:
        payload = issue.model_dump()
        payload["reporter_id"] = reporter_id
        payload["project_id"] = project_id

        return self.repository.create(payload)

    def update_issue(self, issue: IssueUpdate) -> int:
        return self.repository.update(
            issue.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        )

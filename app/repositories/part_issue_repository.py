from sqlalchemy.orm import Session

from app.models.part_issue import (
    PartIssue,
)


class PartIssueRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        issue: PartIssue,
    ):

        self.db.add(
            issue
        )

        self.db.commit()

        self.db.refresh(
            issue
        )

        return issue

    def get_by_id(
        self,
        issue_id: int,
    ):

        return (
            self.db.query(
                PartIssue
            )
            .filter(
                PartIssue.issue_id
                == issue_id
            )
            .first()
        )

    def get_all(
        self,
    ):

        return (
            self.db.query(
                PartIssue
            )
            .order_by(
                PartIssue.issue_id.desc()
            )
            .all()
        )

    def update(
        self,
        issue,
    ):

        self.db.commit()

        self.db.refresh(
            issue
        )

        return issue
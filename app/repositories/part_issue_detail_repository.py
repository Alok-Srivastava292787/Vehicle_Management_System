from sqlalchemy.orm import Session

from app.models.part_issue import (
    PartIssueDetail,
)


class PartIssueDetailRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        detail: PartIssueDetail,
    ):
        self.db.add(detail)

        self.db.commit()

        self.db.refresh(detail)

        return detail

    def get_by_id(
        self,
        issue_detail_id: int,
    ):
        return (
            self.db.query(
                PartIssueDetail
            )
            .filter(
                PartIssueDetail.issue_detail_id
                == issue_detail_id
            )
            .first()
        )

    def get_all(
        self,
    ):
        return (
            self.db.query(
                PartIssueDetail
            )
            .order_by(
                PartIssueDetail.issue_detail_id.desc()
            )
            .all()
        )

    def update(
        self,
        detail,
    ):
        self.db.commit()

        self.db.refresh(detail)

        return detail
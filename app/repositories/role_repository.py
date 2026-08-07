from sqlalchemy.orm import Session

from app.models.security import Role


class UserRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_username(
        self,
        username: str,
    ):

        return (
            self.db.query(Role)
            .filter(
                Role.role_name
                == username
            )
            .first()
        )

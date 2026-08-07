from sqlalchemy.orm import Session

from app.models.security import UserRole


class UserRoleRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_roles_by_user_id(
        self,
        user_id: int,
    ):

        return (
            self.db.query(UserRole)
            .filter(
                UserRole.user_id
                == user_id
            )
            .first()
        )

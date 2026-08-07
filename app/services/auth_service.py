from fastapi import HTTPException   #type: ignore

from app.repositories.user_repository import (
    UserRepository,
)

from app.security.jwt_handler import (
    create_access_token,
)

from app.security.password_handler_bcrypt import (
    verify_password,
)


class AuthService:

    def __init__(
        self,
        repository:
        UserRepository,
    ):

        self.repository = (
            repository
        )

#    def login(
#        self,
#        payload,
#    ):
    def login(
        self,
        username: str,
        password: str,
    ):
        user = (
            self.repository
            .get_by_username(
                username
            )
        )
        if not user:
            raise HTTPException(
                status_code=401,
                detail=
                "Invalid username or password",
            )
        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail=
                "Invalid username or password",
            )
        token = (
            create_access_token(
                user.username
            )
        )

        return {
            "access_token":
                token,
            "token_type":
                "bearer",
            "username":
                user.username,
            "user_id":
                user.user_id,
            "employee_id":
                user.employee_id,
        }
from fastapi import (    Depends,    HTTPException,)    #type: ignore

from fastapi.security import (    OAuth2PasswordBearer,)    #type: ignore
from fastapi.security import (    OAuth2PasswordRequestForm)    #type: ignore
from app.security.jwt_handler import (
    decode_access_token,
)
from app.db.dependencies import get_db
from sqlalchemy.orm import Session

oauth2_scheme = (
    OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/login"
    )
)

def get_current_username(
    token: str = Depends(
        oauth2_scheme
    ),
):

    try:
        print("TOKEN:", token)
        payload = (
            decode_access_token(
                token
            )
        )
        print("PAYLOAD:", payload)
        username = payload.get(
            "sub"
        )

        if not username:

            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        return username

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository
def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(get_db),
):
    
    payload = (decode_access_token(token))
    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
#    db: Session = Depends(get_db),
    user_role_repository=UserRoleRepository(db)
    user = (UserRepository(db).get_by_username(username))
    roles = (user_role_repository.get_roles_by_user_id(user.user_id))
    user.roles=roles.role_id
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )
    return user

from fastapi import (    APIRouter,    Depends,)    #type: ignore
from sqlalchemy.orm import Session
from app.db.dependencies import (get_db,)
from app.schemas.auth_schema import (LoginRequest,)
from app.repositories.user_repository import (UserRepository,)
from app.services.auth_service import (AuthService,)
from app.security.auth_dependency import (get_current_username,oauth2_scheme, get_current_user)
from app.security.jwt_handler import ( decode_access_token )
from fastapi.security import (    OAuth2PasswordRequestForm,)   #type: ignore
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


def get_service(
    db: Session = Depends(
        get_db
    ),
):

    return (
        AuthService(
            UserRepository(
                db
            )
        )
    )


@router.post(
    "/login"
)
#def login(
#    payload:
#    LoginRequest,
#    service:
#    AuthService =
#    Depends(
#        get_service
#    ),
#):
#
#    return service.login(
#        payload
#    )
@router.post("/login")
def login(
    form_data:
    OAuth2PasswordRequestForm =
    Depends(),
    service:
    AuthService =
    Depends(get_service),
):
    return service.login(
    form_data.username,
    form_data.password,
)

#@router.get("/me")
#def me(
#    username: str =
#    Depends(
#        get_current_username
#    ),
#):
#
#    return {
#        "username":
#        username
#    }

#@router.get("/me")
#def me(
#    token: str = Depends(
#        oauth2_scheme
#    )
#):
#
#    print("TOKEN:", token)
#
#    return {
#        "token": token
#    }

@router.get("/me")
def me(
    current_user = Depends(
        get_current_user
    )
):
    return {
        "username":    current_user.username,
        "employee_id": current_user.employee_id,
        "user_id":     current_user.user_id,
        "roles":       current_user.roles,
    }


@router.get("/auth/test")
def test():

    payload = decode_access_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4NjA5MDE5M30.V6VsGYJnzq88XziOZf8BT-M3WxuQmZYIKptp4iLTKiM"
    )

    return payload
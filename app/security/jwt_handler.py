from datetime import (
    datetime,
    timedelta,
)

from jose import jwt    #type: ignore

SECRET_KEY =    "replace-later"
ALGORITHM =    "HS256"
ACCESS_TOKEN_MINUTES =    60

def create_access_token(
    username: str,
):

    payload = {

        "sub": username,

        "exp":
        datetime.utcnow()
        + timedelta(
            minutes=
            ACCESS_TOKEN_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def decode_access_token(
    token: str,
):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
from pydantic import BaseModel  #type: ignore


class LoginRequest(
    BaseModel
):

    username: str

    password: str
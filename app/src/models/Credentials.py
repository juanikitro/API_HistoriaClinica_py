from pydantic import BaseModel


class Credentials(BaseModel):
    user: str
    password: str

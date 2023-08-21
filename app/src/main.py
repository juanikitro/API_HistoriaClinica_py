from fastapi import FastAPI, Request

from .models.Credentials import Credentials
from .models.PersonData import PersonData

from .controllers.find_all_person_data import find_all_person_data
from .controllers.auth import auth, verify_jwt


app = FastAPI()


# login
@app.post("/v1/auth", tags=["authentication"])
def login(credentials: Credentials):
    return auth(credentials)


# main endpoint
@app.get("/v1/person", tags=["person"])
def all_person_data(request: Request, person: PersonData):
    verify_jwt(request.headers.get("Authorization", None)) 

    return find_all_person_data(person)

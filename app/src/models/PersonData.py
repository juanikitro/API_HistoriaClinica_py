from pydantic import BaseModel


class PersonData(BaseModel):
    document_type: str
    document_number: str
    gender: str

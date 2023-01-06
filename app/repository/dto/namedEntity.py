from pydantic import BaseModel


class NamedEntity(BaseModel):
    name: str
    type: str

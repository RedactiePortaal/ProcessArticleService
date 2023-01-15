from typing import Optional

from pydantic import BaseModel


class NamedEntity(BaseModel):
    id: Optional[int]
    name: str
    type: str

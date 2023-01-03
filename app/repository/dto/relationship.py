from typing import Optional
from pydantic import BaseModel

from app.repository.dto.node import Node


class Relationship(BaseModel):
    id: int
    type: str
    source: Node
    target: Node
    properties: Optional[dict] = None

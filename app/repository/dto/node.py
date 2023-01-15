from typing import List, Optional
from pydantic import BaseModel


class Node(BaseModel):
    id: int
    labels: List[str]
    properties: Optional[dict] = None

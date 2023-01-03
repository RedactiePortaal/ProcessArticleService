from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ProcessArticleResponse(BaseModel):
    title: str
    location: str
    description: str
    image: Optional[str] = None
    category: str
    link: str
    pubDate: datetime
    entities: List[str]

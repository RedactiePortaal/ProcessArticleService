from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessArticleRequest(BaseModel):
    title: str
    location: str
    description: str
    image: Optional[str] = None
    category: str
    link: str
    pubDate: datetime

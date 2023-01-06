import json
from typing import List, Optional

from urllib3 import PoolManager

from app.repository.dto.namedEntity import NamedEntity


class NERRepository:
    def __init__(self, httpClient: PoolManager, baseURL: str):
        self.http = httpClient
        self.baseURL = baseURL

    def getNamedEntities(self, text: str) -> Optional[List[List[NamedEntity]]]:
        response = self.http.request('POST', self.baseURL + '/nl/ner-per-sentence', fields={'text': text})
        if not response.status == 200:
            return
        data = json.loads(response.data.decode('utf-8'))
        namedEntities = []
        for sentence in data:
            sentenceEnts = []
            for ent in sentence:
                sentenceEnts.append(NamedEntity(name=ent.name, type=ent.type))
            namedEntities.append(sentenceEnts)
        return namedEntities

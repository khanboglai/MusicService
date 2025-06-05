import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from typing import Literal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

es = Elasticsearch(f"http://elasticsearch:9200")

SEARCH_SIZE = 10

async def search_for(what: Literal["albums", "tracks", "artists"], phrase: str, page: int):
    """ Поиск в Elasticsearch """
    response = es.search(
        index=what,
        body={
            "from": (page - 1) * SEARCH_SIZE,
            "size": SEARCH_SIZE,
            "query": {
                "match_phrase_prefix": {
                    "title": phrase 
                }
            }
        }
    )
    return response["hits"]["hits"]
import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from typing import Literal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

es = Elasticsearch(f"http://elasticsearch:9200")

SEARCH_SIZE = 10

async def add_artist_to_es(artist_id: int, title: str):
    """ Добавляет альбом в Elasticsearch """
    
    document = {
        "title": title
    }
    response = es.index(index="artists", id=artist_id, document=document)
    logger.info(f"Исполнитель с ID {artist_id} добавлен в Elasticsearch")
    return response

async def rmv_artist_from_es(artist_id: int):
    """ Удаляет альбом из Elasticsearch """

    response = es.delete(index="artists", id=artist_id)
    logger.info(f"Исполнитель с ID {artist_id} удален из Elasticsearch")
    return response

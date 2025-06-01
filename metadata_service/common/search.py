import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from typing import Literal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

es = Elasticsearch(f"http://elasticsearch:9200")

SEARCH_SIZE = 10

async def add_album_to_es(album_id: int, title: str):
    """ Добавляет альбом в Elasticsearch """
    
    document = {
        "title": title
    }
    response = es.index(index="albums", id=album_id, document=document)
    logger.info(f"Альбом с ID {album_id} добавлен в Elasticsearch")
    return response

async def rmv_album_from_es(album_id: int):
    """ Удаляет альбом из Elasticsearch """

    response = es.delete(index="albums", id=album_id)
    logger.info(f"Альбом с ID {album_id} удален из Elasticsearch")
    return response

async def add_track_to_es(track_id: int, title: str):
    """ Добавляет трек в Elasticsearch """

    document = {
        "title": title
    }
    response = es.index(index="tracks", id=track_id, document=document)
    logger.info(f"Трек с ID {track_id} добавлен в Elasticsearch")
    return response

async def rmv_track_from_es(track_id: int):
    """ Удаляет трек из Elasticsearch """

    response = es.delete(index="tracks", id=track_id)
    logger.info(f"Трек с ID {track_id} удален из Elasticsearch")
    return response

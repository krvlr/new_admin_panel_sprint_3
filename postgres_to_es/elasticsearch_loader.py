from http import HTTPStatus

from decorators import backoff
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from es_schema import MOVIES_INDEX
from loguru import logger
from models import ESFilmworkData
from settings import ELASTIC_SEARCH_URL


class ElasticsearchLoader:
    def __init__(self):
        self.client = self._create_connection()
        self._create_index()

    @backoff()
    def _create_connection(self):
        return Elasticsearch(ELASTIC_SEARCH_URL)

    @backoff()
    def _create_index(self) -> None:
        if not self.client.indices.exists(index="movies"):
            self.client.indices.create(
                index="movies",
                ignore=HTTPStatus.BAD_REQUEST.value,
                body=MOVIES_INDEX,
            )
            logger.debug("Индекс для movies создан")

    @backoff()
    def load_movies(self, data: list[ESFilmworkData]) -> None:
        documents = [
            {"_index": "movies", "_id": row.id, "_source": row.dict()} for row in data
        ]
        bulk(self.client, documents)

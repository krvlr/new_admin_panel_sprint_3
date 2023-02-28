from datetime import datetime
from typing import Iterator

import psycopg2
from decorators import backoff
from loguru import logger
from psycopg2.extras import RealDictCursor
from settings import ETL_BATCH_SIZE, POSTGRES_CONNECTION_SETTINGS

FILMWORKS_QUERY = """
        SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating,
            fw.type,
            fw.created,
            fw.modified,
            COALESCE (
                    json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        array_agg(DISTINCT g.name) as genres
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.modified > %s OR p.modified > %s OR g.modified > %s
        GROUP BY fw.id
        """


class PostgresExtractor:
    def __init__(self):
        self.connection = self._create_connection()
        self.cursor = self.connection.cursor()

    @backoff()
    def _create_connection(self):
        return psycopg2.connect(
            **POSTGRES_CONNECTION_SETTINGS, cursor_factory=RealDictCursor
        )

    @backoff()
    def extract_movies(self, date_last_modified: datetime) -> Iterator:
        self.cursor.execute(FILMWORKS_QUERY, (date_last_modified,) * 3)
        while rows := self.cursor.fetchmany(ETL_BATCH_SIZE):
            yield rows

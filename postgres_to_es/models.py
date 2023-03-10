from typing import Optional

from pydantic import BaseModel


class ESPersonData(BaseModel):
    id: str
    name: str


class ESFilmworkData(BaseModel):
    id: str
    imdb_rating: Optional[float]
    genre: list[str] = []
    title: str
    description: Optional[str]
    director: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[ESPersonData] = []
    writers: list[ESPersonData] = []

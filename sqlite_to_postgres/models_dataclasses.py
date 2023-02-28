import inspect
import uuid
from abc import ABCMeta
from dataclasses import dataclass
from datetime import date


class BaseModel:
    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )


@dataclass(frozen=True)
class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: str


@dataclass(frozen=True)
class Filmwork(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    creation_date: date
    type: str
    rating: float = 0
    certificate: str = None
    file_path: str = None


@dataclass(frozen=True)
class GenreFilmwork(BaseModel):
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID


@dataclass(frozen=True)
class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    gender: str = None


@dataclass(frozen=True)
class PersonFilmwork(BaseModel):
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str


TABLE_NAME_DATACLASS_MAPPING = {
    "genre": Genre,
    "person": Person,
    "film_work": Filmwork,
    "genre_film_work": GenreFilmwork,
    "person_film_work": PersonFilmwork,
}

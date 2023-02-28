import uuid
from enum import Enum

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'

        indexes = [
            models.Index(
                fields=["film_work_id", "genre_id"],
                name="genre_film_work",
            ),
        ]


class Gender(models.TextChoices):
    MALE = "male", _("male")
    FEMALE = "female", _("female")


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255, unique=True)
    gender = models.TextField(_("gender"), choices=Gender.choices, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class RoleType(models.TextChoices):
    ACTOR = "actor", _("Actor")
    DIRECTOR = "director", _("Dicrector")
    WRITER = "writer", _("Writer")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    role = models.TextField(_("role"), choices=RoleType.choices, null=True)

    class Meta:
        db_table = 'content"."person_film_work'

        indexes = [
            models.Index(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_idx",
            ),
        ]


class Filmwork(UUIDMixin, TimeStampedMixin):
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"))
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")
    certificate = models.CharField(
        _("certificate"), max_length=512, blank=True, null=True
    )
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")

    class Type(models.TextChoices):
        MOVIE = "movie", _("Movie")
        TV_show = "tv_show", _("TV show")

    type = models.CharField(
        _("type"), max_length=20, choices=Type.choices, default=Type.MOVIE
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film work")
        verbose_name_plural = _("Film works")

        indexes = [
            models.Index(
                fields=["title", "creation_date"],
                name="film_work_title_date",
            ),
            models.Index(
                fields=["type", "rating", "creation_date"],
                name="film_work_type_rating_date",
            ),
        ]

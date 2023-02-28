from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

    search_fields = ("name", "description")


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

    autocomplete_fields = ("genre",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name",)

    search_fields = ("full_name",)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

    autocomplete_fields = ("person",)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = ("title", "type", "creation_date", "rating", "created", "modified")

    list_filter = ("type", "genres")

    search_fields = ("title", "description")

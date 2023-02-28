from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, RoleType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def _aggregate_person(self, role):
        return ArrayAgg(
            "personfilmwork__person__full_name",
            distinct=True,
            filter=Q(personfilmwork__role=role),
        )

    def get_queryset(self):
        qs = super(MoviesApiMixin, self).get_queryset()
        qs = qs.prefetch_related("genres", "persons")
        qs = qs.values("id", "title", "description", "creation_date", "rating", "type")
        qs = qs.annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=self._aggregate_person(RoleType.ACTOR),
            directors=self._aggregate_person(RoleType.DIRECTOR),
            writers=self._aggregate_person(RoleType.WRITER),
        )
        return qs

    def render_to_response(self, context):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = list(self.get_queryset())
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, settings.MOVIES_PER_PAGE_COUNT
        )
        prev_page = page.previous_page_number() if page.has_previous() else None
        next_page = page.next_page_number() if page.has_next() else None
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": queryset,
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return self.object

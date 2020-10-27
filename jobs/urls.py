from django.urls import path
from jobs.views import JobsView, FilterResultsView
from jobs.views import SearchResultsView
from . import views
from .filters import JobFilter

app_name = "jobs"

urlpatterns = [
    path("", JobsView.as_view(), name="jobs"),
    path("search/", SearchResultsView.as_view(), name="results"),
    path("filter/", SearchResultsView.as_view(), name="filter"),
]

from django.urls import path
from jobs.views import JobsView
from jobs.views import SearchResultsView, SearchFilterView

app_name = "jobs"
urlpatterns = [
    path("", JobsView.as_view(), name="jobs"),
    path("search/", SearchResultsView.as_view(), name="results"),
    path("filter/", SearchFilterView.as_view(), name="filter"),
]

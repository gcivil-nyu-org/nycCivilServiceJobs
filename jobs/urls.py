from django.urls import path
from jobs.views import JobsView
from jobs.views import SearchResultsView, SaveJobsView, SearchFilterView

app_name = "jobs"
urlpatterns = [
    path("", JobsView.as_view(), name="jobs"),
    path("search/", SearchResultsView.as_view(), name="results"),
    path("<int:pk>/saveJob", SaveJobsView.as_view(), name="saveJob"),
    path("filter/", SearchFilterView.as_view(), name="filter"),
]

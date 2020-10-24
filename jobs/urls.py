from django.urls import path
from jobs.views import JobsView

app_name = "jobs"
urlpatterns = [
    path("", JobsView.as_view(), name="jobs"),
]

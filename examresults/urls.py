from django.urls import path
from examresults.views import ExamsActiveView

app_name = "examresults"
urlpatterns = [
    path("", ExamsActiveView.as_view(), name="exams"),
]

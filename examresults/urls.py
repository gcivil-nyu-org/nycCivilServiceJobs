from django.urls import path
from examresults.views import ExamsActiveView, ExamJSON

app_name = "examresults"
urlpatterns = [
    path("", ExamsActiveView.as_view(), name="exams"),
    path("data/<str:q>", ExamJSON.as_view(), name="exams_data"),
    path("data", ExamJSON.as_view(), name="exams_data"),
]

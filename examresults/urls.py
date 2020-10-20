from django.urls import path
from examresults.views import *
from django.views.generic import TemplateView

app_name = 'examresults'
urlpatterns = [
    path('', ExamsActiveView.as_view(), name='exams'),
]

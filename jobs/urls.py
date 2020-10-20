from django.urls import path
from jobs.views import JobsView
from django.views.generic import TemplateView

app_name = 'jobs'
urlpatterns = [
    path('', JobsView.as_view(), name='jobs'),
]
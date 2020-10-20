from django.shortcuts import render
from django.views.generic import TemplateView
from .models import job_record


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"
    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all(),
        }
        return context
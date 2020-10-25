from django.views.generic import TemplateView, ListView
from .models import job_record
from django.db.models import Q


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all(),
        }
        return context


class SearchResultsView(ListView):
    model = job_record
    template_name = "jobs/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = job_record.objects.filter(
            Q(agency__icontains=query)
            | Q(business_title__icontains=query)
            | Q(civil_service_title__icontains=query)
        )
        return object_list

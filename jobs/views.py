from django.views.generic import TemplateView, ListView
from .filters import JobFilter
from .models import job_record
from django.db.models import Q


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all().order_by("posting_date").reverse()[:10],
        }
        return context


class SearchResultsView(ListView):
    model = job_record
    template_name = "jobs/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if not query:

            def get_context_data(self, *args, **kwargs):
                context = {
                    "jobs": job_record.objects.all()
                    .order_by("posting_date")
                    .reverse()[:10],
                }
                return context

        else:
            object_list = job_record.objects.filter(
                Q(agency__icontains=query)
                | Q(business_title__icontains=query)
                | Q(civil_service_title__icontains=query)
            )
            return object_list


class FilterResultsView(ListView):
    filterset_class = JobFilter
    context_object_name = "jobs_filter"
    template_name = "jobs/search_filter.html"
    queryset = job_record.objects.all()

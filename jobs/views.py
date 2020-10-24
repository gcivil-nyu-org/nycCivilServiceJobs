from django.shortcuts import render
from django.views.generic import TemplateView
from .models import job_record
from django.db.models import Q, Count
from django.shortcuts import render
# import django_filters

class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all(),
        }
        return context

    def filter_view(request):
        qs = job_record.objects.all()
        civil_service_title = request.GET.get('civil_service_title')
        job_id = request.GET.get('job_id')
        business_title = request.GET.get('business_title')
        salary_range_from = request.GET.get('salary_range_from')
        salary_range_to = request.GET.get('salary_range_to')
        posting_date = request.GET.get('posting_date')
        post_until = request.GET.get('post_until')
        career_level = request.GET.get('career_level')
        full_time_part_time_indicator = request.GET.get('full_time_part_time_indicator')

        if civil_service_title != '' and civil_service_title is not None:
            qs = qs.filter(title__icontains=civil_service_title)

        if job_id != '' and job_id is not None:
            qs = qs.filter(title__icontains=job_id)

        # print(qs)
        context = {
            'queryset': qs,
        }
        return render(request, "jobs/jobs.html", context)
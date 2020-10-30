from django.views.generic import TemplateView, ListView
from .models import job_record
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all().order_by("posting_date").reverse()[:10],
        }
        return context

    @login_required
    def add_favorite(request, id):
        job = get_object_or_404(job_record, id=id)
        if job.favorites.filter(id=request.user.id).exists():
            job.favorites.remove(request.user)
        else:
            job.favorites.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    @login_required
    def favorite_list(request):
        new = job_record.newmanager.filter(favorites=request.user)
        return render(request,
                      'jobs/favorites.html',
                      {'new': new})

    def job_single(request, job):
        job = get_object_or_404(job_record)
        is_fav = bool

        if job.favorites.filter(id=request.user.id).exists():
            is_fav = True

        return render(request, 'jobs/jobs.html', {'job': job, 'is_fav': is_fav})


class SearchResultsView(ListView):
    model = job_record
    template_name = "jobs/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        object_list = job_record.objects.filter(
            Q(agency__icontains=query)
            | Q(business_title__icontains=query)
            | Q(civil_service_title__icontains=query)
        )
        return object_list

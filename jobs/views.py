from django.shortcuts import render
from django.views.generic import TemplateView
from .getdata import getJobs

from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from register.forms import SignUpForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

class GetData(TemplateView):
    template_name = 'jobs.html'
    def get_context_data(self, *args, **kwargs):
        context = {
            'jobs' : getJobs(),
        }
        return context
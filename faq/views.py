from django.shortcuts import render
from .models import faq
from django.views.generic import TemplateView

# Create your views here.

class FAQView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        context = {
            "faqs": faq.objects.all()
            }

        return render(
            request=request,
            template_name="faq/faqs.html",
            context=context
        )
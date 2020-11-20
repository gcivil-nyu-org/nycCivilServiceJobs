from django.conf import settings
from django.contrib.sites.models import Site


class DynamicSiteDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)
            current_site.domain = request.get_host()
            current_site.save()
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)

        request.current_site = current_site
        settings.SITE_ID = 1

        response = self.get_response(request)
        return response

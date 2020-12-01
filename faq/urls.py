
from django.urls import path
from faq.views import FAQView


app_name = "faq"
urlpatterns = [
    path("", FAQView.as_view(), name="faq")]
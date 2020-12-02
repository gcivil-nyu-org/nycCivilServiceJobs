from django.urls import path
from contactus.views import ContactUsView

app_name = "contactus"
urlpatterns = [
    path("", ContactUsView.as_view(), name="contactus"),
]

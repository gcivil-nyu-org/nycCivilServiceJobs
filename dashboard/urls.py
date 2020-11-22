# nycCivilServiceJobs URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.urls import path
from dashboard.views import (
    DashboardView,
    SavedJobs,
    SubscriptionView,
    SaveUpcomingExamView,
    SaveExamNumberView,
    DeleteUpcomingExamView,
    DeleteExamResultsView,
    ExpiredSubscriptionView,
)


app_name = "dashboard"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("savedjobs", SavedJobs.as_view(), name="savedjobs"),
    path("subscription", SubscriptionView.as_view(), name="subscription"),
    path(
        "SaveUpcomingExamView",
        SaveUpcomingExamView.as_view(),
        name="SaveUpcomingExamView",
    ),
    path(
        "SaveExamNumberView",
        SaveExamNumberView.as_view(),
        name="SaveExamNumberView",
    ),
    path(
        "CivilServiceTitleDelete",
        DeleteUpcomingExamView.as_view(),
        name="DeleteUpcomingExamView",
    ),
    path(
        "ExamResultsDelete",
        DeleteExamResultsView.as_view(),
        name="DeleteExamResultsView",
    ),
    path(
        "expiredsubscription",
        ExpiredSubscriptionView.as_view(),
        name="expiredsubscription",
    ),
]

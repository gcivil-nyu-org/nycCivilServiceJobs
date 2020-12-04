"""nycCivilServiceJobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from signin.views import UserProfileView
from dashboard.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("register/", include("register.urls")),
    path("signin/", include("signin.urls")),
    path("jobs/", include("jobs.urls")),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("exams/", include("examresults.urls")),
    path("profile/", UserProfileView.as_view(), name="userprofile"),
    path("dashboard/", include("dashboard.urls")),
]

handler400 = "signin.views.handler400"
handler403 = "signin.views.handler403"
handler404 = "signin.views.handler404"
handler500 = "signin.views.handler500"

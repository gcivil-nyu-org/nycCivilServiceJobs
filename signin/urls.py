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

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from signin.views import SignInView, SaveCivilServiceTitleView

app_name = "signin"
urlpatterns = [
    path("", SignInView.as_view(), name="signin"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="signin/password_reset.html",
            email_template_name="signin/password_reset_email.html",
            success_url=reverse_lazy("signin:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="signin/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="signin/password_reset_confirm.html",
            success_url=reverse_lazy("signin:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="signin/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "SaveCivilServiceTitleView",
        SaveCivilServiceTitleView.as_view(),
        name="SaveCivilServiceTitleView",
    ),
]

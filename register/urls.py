from django.urls import path
from register.views import SignUpView
from django.views.generic import TemplateView

app_name = 'register'
urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('success', TemplateView.as_view(template_name='success.html'), name='success'),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'), 
]
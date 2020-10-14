from django.urls import path
from register.views import SignUpView, SuccessView
from django.views.generic import TemplateView

app_name = 'register'
urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('success', SuccessView.as_view(), name='success'),
    path('home', TemplateView.as_view(template_name='register/success.html'), name='home'), 
]
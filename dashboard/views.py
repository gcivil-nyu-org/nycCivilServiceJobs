from django.shortcuts import render
from django.contrib.auth import *
# Create your views here.
def index(request):
        return render(request = request,
                        template_name = "index.html",
                        context={"user":request.user})

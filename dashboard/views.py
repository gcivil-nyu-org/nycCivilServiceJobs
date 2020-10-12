from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/signin')
def index(request):
        return render(request = request,
                        template_name = "index.html",
                        context={"user":request.user})

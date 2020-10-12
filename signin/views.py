from django.shortcuts import render,redirect,reverse
from django.contrib.auth.forms import *
from django.contrib.auth import *
from django.contrib import messages
from django.views.generic import *

class SignInView(FormView):
    form_class = AuthenticationForm
    template_name = 'signin/signin.html'

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.info(self.request, f"You are now logged in as {username}")
            return redirect(reverse('index'))
        else:
            messages.error(self.request, "Invalid username or password.")
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return super(SignInView, self).get(request, *args, **kwargs)

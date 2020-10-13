# Create your views here.

from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView
from register.forms import SignUpForm
from django.core.mail import EmailMessage
from django.contrib import messages


# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('register:success')
    template_name = 'signup.html'

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """

        first_name = form.cleaned_data.get("first_name")

        message = render_to_string(
            "register/account_activated.html",
        )

        email_subject = "Your account has been activated"
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()

        return super(SignUpView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "User is already registered!")
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return super(SignUpView, self).get(request, *args, **kwargs)

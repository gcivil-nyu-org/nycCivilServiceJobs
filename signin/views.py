from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import FormView
from django.views import View
from jobs.models import UserSavedJob


class SignInView(FormView):
    form_class = AuthenticationForm
    template_name = "signin/signin.html"

    def form_valid(self, form):
        # """
        # The user has provided valid credentials
        # (this was checked in AuthenticationForm.is_valid()).
        # So now we can log him in.
        # """
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            # messages.info(self.request, f"You are now logged in as {username}")
            return redirect(reverse("signin:success"))
        else:
            messages.error(self.request, "Invalid username or password.")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form)
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("signin:success"))
        return super(SignInView, self).get(request, *args, **kwargs)


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        
        user_saved_jobs = UserSavedJob.objects.filter(user=self.request.user)
        saved_jobs_user = list(user_saved_jobs.values_list("job", flat=True ))
        jobs = map(lambda x: x.job, user_saved_jobs)

        return render(
            request=request,
            template_name="signin/success.html",
            context={"user": request.user, "jobs":jobs, "saved_jobs_user":saved_jobs_user},
        )

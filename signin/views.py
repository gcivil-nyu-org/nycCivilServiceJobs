from django.shortcuts import redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.http import is_safe_url
from django.views.generic import FormView


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
        nxt = self.request.POST.get("next")

        print(self.request)
        if user is not None:
            login(self.request, user)
            if nxt is None:
                return redirect("dashboard:dashboard")
            elif not is_safe_url(
                url=nxt,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure(),
            ):
                return redirect("dashboard:dashboard")
            else:
                return redirect(nxt)

                # messages.info(self.request, f"You are now logged in as {username}")
        else:
            messages.error(self.request, "Invalid username or password.")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form)
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard:dashboard"))
        return super(SignInView, self).get(request, *args, **kwargs)

from django.http.response import JsonResponse
from django.shortcuts import redirect, reverse, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.http import is_safe_url
from django.views.generic import FormView
from django.views import View
from signin.forms import UserProfileForm
from examresults.models import CivilServicesTitle
from signin.models import UsersCivilServiceTitle
import json
from django.core.exceptions import (
    PermissionDenied,
    SuspiciousOperation,
    ObjectDoesNotExist,
)
from django.http import Http404


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
            nxt = self.request.GET.get("next")
            # print(nxt)
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
        return super(SignInView, self).get(request, *args, **kwargs)


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile_form = UserProfileForm(instance=request.user)
            civil_services_title_all = CivilServicesTitle.objects.all()
            user_civil_services_title = UsersCivilServiceTitle.objects.filter(
                user=self.request.user
            )
            user_curr_civil_services_title = list(
                user_civil_services_title.filter(is_interested=False).values_list(
                    "civil_service_title", flat=True
                )
            )
            user_interested_civil_services_title = list(
                user_civil_services_title.filter(is_interested=True).values_list(
                    "civil_service_title", flat=True
                )
            )

            # print(current_civil_services_title_list)
            # print(interested_civil_services_title_list)
            return render(
                request,
                "signin/user_profile.html",
                context={
                    "user": request.user,
                    "form": profile_form,
                    "civil_services_title_all": civil_services_title_all,
                    "user_curr_civil_services_title": json.dumps(
                        user_curr_civil_services_title
                    ),
                    "user_interested_civil_services_title": json.dumps(
                        user_interested_civil_services_title
                    ),
                },
            )
        else:
            return redirect(reverse("signin:signin"))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            civil_services_title_all = CivilServicesTitle.objects.all()
            user_civil_services_title = UsersCivilServiceTitle.objects.filter(
                user=self.request.user
            )
            user_curr_civil_services_title = list(
                user_civil_services_title.filter(is_interested=False).values_list(
                    "civil_service_title", flat=True
                )
            )
            user_interested_civil_services_title = list(
                user_civil_services_title.filter(is_interested=True).values_list(
                    "civil_service_title", flat=True
                )
            )

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, ("Your profile was successfully updated"))
                return redirect("userprofile")
            else:
                return render(
                    request=request,
                    template_name="signin/user_profile.html",
                    context={
                        "user": request.user,
                        "form": profile_form,
                        "civil_services_title_all": civil_services_title_all,
                        "user_curr_civil_services_title": json.dumps(
                            user_curr_civil_services_title
                        ),
                        "user_interested_civil_services_title": json.dumps(
                            user_interested_civil_services_title
                        ),
                    },
                )
        else:
            return redirect(reverse("signin:signin"))


class SaveCivilServiceTitleView(View):
    def post(self, request, *args, **kwargs):

        # print(request.POST['jobs_pk_id'])
        if self.request.method == "POST":
            user_int_cst = list(request.POST.getlist("user_int_cst[]"))
            user_curr_cst = list(request.POST.getlist("user_curr_cst[]"))
            response_data = {}
            user = request.user
            if user.is_authenticated:

                response_data = {
                    "count_before": UsersCivilServiceTitle.objects.filter(
                        user=user
                    ).count()
                }

                UsersCivilServiceTitle.objects.filter(user=user).delete()

                for cst in user_curr_cst:
                    civilServiceTitle = CivilServicesTitle.objects.get(pk=cst)
                    already_saved = UsersCivilServiceTitle.objects.filter(
                        user=user, civil_service_title=civilServiceTitle
                    )
                    if already_saved.count() == 0:
                        save_civilServiceTitle = UsersCivilServiceTitle(
                            user=user,
                            civil_service_title=civilServiceTitle,
                            is_interested=False,
                        )
                        save_civilServiceTitle.save()

                for int_cst in user_int_cst:
                    int_civilServiceTitle = CivilServicesTitle.objects.get(pk=int_cst)
                    already_saved_int = UsersCivilServiceTitle.objects.filter(
                        user=user, civil_service_title=int_civilServiceTitle
                    )
                    if already_saved_int.count() == 0:
                        save_int_civilServiceTitle = UsersCivilServiceTitle(
                            user=user,
                            civil_service_title=int_civilServiceTitle,
                            is_interested=True,
                        )
                        save_int_civilServiceTitle.save()

                # print("inside post")
                user_civil_services_title = UsersCivilServiceTitle.objects.filter(
                    user=user
                )
                user_curr_civil_services_title = list(
                    user_civil_services_title.filter(is_interested=False).values_list(
                        "civil_service_title", flat=True
                    )
                )
                user_interested_civil_services_title = list(
                    user_civil_services_title.filter(is_interested=True).values_list(
                        "civil_service_title", flat=True
                    )
                )

                response_data["user_curr_civil_services_title"] = json.dumps(
                    user_curr_civil_services_title
                )
                response_data["user_interested_civil_services_title"] = json.dumps(
                    user_interested_civil_services_title
                )
                response_data["response_data"] = "CST_SAVED"
                return JsonResponse(response_data, status=200)

            else:
                # messages.error(self.request, "Invalid username or password.")
                # print ('inside post else')
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)


def permission_denied_view(request):
    raise PermissionDenied


def not_found_view(request):
    raise Http404()


def bad_request_view(request):
    raise SuspiciousOperation


def server_error_view(request):
    raise ObjectDoesNotExist


def handler404(request, *args, **argv):
    context = {"code": 404}
    return render(request, "errors/errors.html", context=context)


def handler403(request, *args, **argv):
    context = {"code": 403}
    return render(request, "errors/errors.html", context=context)


def handler400(request, *args, **argv):
    context = {"code": 400}
    return render(request, "errors/errors.html", context=context)


def handler500(request, *args, **argv):
    context = {"code": 500}
    return render(request, "errors/errors.html", context=context)

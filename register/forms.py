from django import forms
from register.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# Sign Up Form


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    username = forms.CharField(max_length=30)
    CHOICES_AT = [(False, "Job Seeker"), (True, "Hiring Manager")]
    # is_hiring_manager = forms.ChoiceField(
    #     choices=CHOICES_AT, label="Account Type", widget=forms.Select(), required=True
    # )
    dob = forms.DateField(
        label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = [
            # "is_hiring_manager",
            "username",
            "first_name",
            "last_name",
            "dob",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "This Email is already registered. "
                "Please use a different email address."
            )
        # Hiring Manager module will be put on freeze as there are no
        # feature that distingushes them from Job seeker until they are
        # able to post for Jobs

        # is_hiring_manager = False
        # email_domain = email[-4:]
        # if is_hiring_manager == "True" and email_domain != ".gov":
        #     raise ValidationError(
        #         "This email is not a valid Email Address for Hiring Manager. "
        #         "Please use a different email address."
        #     )
        return self.cleaned_data.get("email")

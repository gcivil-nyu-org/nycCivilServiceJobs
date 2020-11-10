from crispy_forms.layout import Submit
from django import forms
from register.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper

# Sign Up Form


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    username = forms.CharField(max_length=30, widget=forms.HiddenInput())
    CHOICES_AT = [(False, "Job Seeker"), (True, "Hiring Manager")]
    is_hiring_manager = forms.ChoiceField(
        choices=CHOICES_AT, label="Account Type", widget=forms.Select(), required=True
    )
    dob = forms.DateField(
        label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = [
            "is_hiring_manager",
            "username",
            "first_name",
            "last_name",
            "dob",
            "email",
        ]

    is_hiring_manager.disabled = True
    username

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        username = self.cleaned_data.get("username")

        if User.objects.exclude(username=username).filter(email=email).exists():
            raise ValidationError(
                "This Email is already in use for some other account. "
                "Please use a different email address."
            )

        is_hiring_manager = self.cleaned_data.get("is_hiring_manager")
        email_domain = email[-4:]
        if is_hiring_manager == "True" and email_domain != ".gov":
            raise ValidationError(
                "This email is not a valid Email Address for Hiring Manager. "
                "Please use a different email address."
            )
        return self.cleaned_data.get("email")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.add_input(Submit("submit", "Update Profile"))

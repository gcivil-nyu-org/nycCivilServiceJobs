from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# from signin.models import User


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]

        # Checks whether the email exists in the database for password reset or not.
        # Also checks whether the user have an active account or not.

        if User.objects.filter(email__iexact=email, is_active=False).exists():
            raise ValidationError(
                "You need to activate your account first."
                "Please check your email."
            )

        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError(
                "There is no user registered with the specified E-Mail address."
                "Please check your email."
            )

        return email

from django import forms
from register.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError

# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    username = forms.CharField(max_length=30)
    CHOICES_SQ = [('MN', "What is Your Mother\'s maiden name"),
                  ('VS', "What is your favorite vacation spot?"),
                  ('NM', "What was your childhood nickname?"),
                  ('CF', "What is the name of your favorite childhood friend?"),
                  ('FJ', "In what city or town was your first job?")]

    security_ques = forms.CharField(
        label='Security Question', widget=forms.Select(choices=CHOICES_SQ))
    security_ans = forms.CharField(label='Answer', max_length=100)
    CHOICES_AT = [(False, 'Job Seeker'), (True, 'Hiring Manager')]
    is_hiring_manager = forms.ChoiceField(choices=CHOICES_AT, label="Account Type",
                                          widget=forms.Select(), required=True)
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = User
        fields = [
            'is_hiring_manager',
            'username',
            'first_name',
            'last_name',
            'dob',
            'email',
            'password1',
            'password2',
            'security_ques',
            'security_ans',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "This Email is already registered. Please use a different email address.")

        account_type = self.cleaned_data.get('acc_type')
        email_domain = email[-4:]
        if account_type == 'hm' and email_domain != '.gov':
            raise ValidationError(
                "This email is not a valid Email Address for Hiring Manager. Please use a different email address.")
        return self.cleaned_data.get('email')

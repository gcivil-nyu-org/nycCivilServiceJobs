from django import forms
from django.contrib.auth.models import User
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

    security_ques = forms.CharField(label='Security Question', widget=forms.Select(choices=CHOICES_SQ))
    security_ans = forms.CharField(label='Answer', max_length=100)
    CHOICES_AT = [('js', 'Job Seeker'),
                  ('hm', 'Hiring Manager')]

    acc_type = forms.CharField(label='Account Type', widget=forms.Select(choices=CHOICES_AT))
    dob = forms.DateField(label='Date of Birth')

    class Meta:
        model = User
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        fields = [
            'acc_type',
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

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")

        account_type = self.cleaned_data.get('acc_type')
        email_domain = email[-4:]
        if account_type == 'hm' and email_domain != '.gov':
            raise ValidationError("Not a valid Email for Hiring Manager")
        return self.cleaned_data

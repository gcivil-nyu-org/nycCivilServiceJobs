from django import forms

from contactus.models import ContactUsModel


# Contact Us Form


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=64)
    email = forms.EmailField()
    subject = forms.CharField(max_length=1000)
    message = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = ContactUsModel
        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]

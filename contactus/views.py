from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.views.generic import CreateView
from contactus.forms import ContactUsForm
from django.core.mail import EmailMessage
from django.contrib import messages


class ContactUsView(CreateView):
    form_class = ContactUsForm
    # success_url = reverse_lazy("contactus:contactus")
    template_name = "contactus/contactus.html"

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        message_str = form.cleaned_data.get("message")

        message = render_to_string(
            "contactus/contactform_submitted.html",
            {
                "name": name,
                "message_str": message_str,
            },
        )

        email_subject = "We have received your message"
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()

        message_admin = render_to_string(
            "contactus/contactform_admin.html",
            {
                "user": name,
                "message_str": message_str,
            },
        )

        email_subject_admin = "A request has been submitted"
        to_email_admin = "nyccivilservice.csgy6063@gmail.com"
        email_admin = EmailMessage(email_subject_admin, message_admin, to=[to_email_admin])
        email_admin.send()

        return super(ContactUsView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Your request has been submitted')

        return reverse('contactus:contactus')

from django.test import TestCase
from django.urls import reverse, resolve
from contactus.forms import ContactUsForm
from contactus.models import ContactUsModel
from contactus.apps import ContactUsConfig
from contactus.views import ContactUsView
from django.contrib.messages import get_messages


class TestContactUs(TestCase):
    def setUp(self):
        self.contactus_url = reverse("contactus:contactus")

        self.contactus_form_data = ContactUsModel(
            contact_id=1,
            name="John Doe",
            email="john.doe@gmail.com",
            subject="Test subject",
            message="Hi this is a test message",
        )
        self.contactus_form_data.save()
        return super().setUp

    def test_contactus_apps(self):
        self.assertEqual(ContactUsConfig.name, "contactus")

    def test_contactus_form_is_valid(self):
        form = ContactUsForm(
            data={
                "contact_id": "1",
                "name": "John Doe",
                "email": "john.doe@gmail.com",
                "subject": "Test subject",
                "message": "Hi this is a test message",
            },
        )
        self.assertTrue(form.is_valid())

    def test_contactus_form_is_invalid(self):
        form = ContactUsForm(
            data={},
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_contactus_view_correct_template_loaded(self):
        # To test if correct Contact us page is loaded
        get_response = self.client.get(self.contactus_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "contactus/contactus.html")

        post_response = self.client.get(self.contactus_url)
        self.assertEqual(post_response.status_code, 200)
        self.assertTemplateUsed(post_response, "contactus/contactus.html")

        # Another way to test if correct Contact us page is loaded
        test_contactus_url = reverse("contactus:contactus")
        self.assertEqual(resolve(test_contactus_url).func.view_class, ContactUsView)

    def test_contactus_view_correct_response_shown(self):
        response = self.client.post(
            self.contactus_url,
            data={
                "contact_id": "1",
                "name": "John Doe",
                "email": "john.doe@gmail.com",
                "subject": "Test subject",
                "message": "Hi this is a test message",
            },
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Your request has been submitted", messages)

    def test_contactus_view_number_of_forms_sent(self):
        forms_count = ContactUsModel.objects.count()

        response = self.client.post(
            self.contactus_url,
            data={
                "contact_id": "1",
                "name": "John Doe",
                "email": "john.doe@gmail.com",
                "subject": "Test subject",
                "message": "Hi this is a test message",
            },
        )

        forms_count = forms_count + 1
        self.assertEqual(ContactUsModel.objects.count(), forms_count)
        self.assertEqual(response.status_code, 302)

    def test_contactus_view_email_sent(self):
        response = self.client.post(
            self.contactus_url,
            data={
                "contact_id": "1",
                "name": "John Doe",
                "email": "john.doe@gmail.com",
                "subject": "Test subject",
                "message": "Hi this is a test message",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "contactus/contactform_submitted.html")
        self.assertRedirects(
            response, reverse("contactus:contactus"), fetch_redirect_response=True
        )

    def test_contactus_view_email_admin_sent(self):
        response = self.client.post(
            self.contactus_url,
            data={
                "contact_id": "1",
                "name": "John Doe",
                "email": "john.doe@gmail.com",
                "subject": "Test subject",
                "message": "Hi this is a test message",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "contactus/contactform_admin.html")
        self.assertRedirects(
            response, reverse("contactus:contactus"), fetch_redirect_response=True
        )

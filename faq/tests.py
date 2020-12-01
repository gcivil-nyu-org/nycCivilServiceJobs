from django.test import TestCase
from django.urls import reverse
from faq.models import faq


class FAQTest(TestCase):
    def setUp(self):
        # set up fake faq quesirons
        for i in range(2):
            entry = faq(
                question=str(i) + "What is Civil Service?",
                answer=str(i) + "This is Civil Service.",
            )
            entry.save()

    def test_faq_view_correct_template_loaded(self):
        # correct Faq page is loaded
        response = self.client.get(reverse("faq:faq"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/faqs.html")

    def test_faq_view_correct_number_of_question_loaded(self):
        response = self.client.get(reverse("faq:faq"))
        expected_faq = list(faq.objects.all())
        actual_faq = list(response.context["faqs"])
        self.assertEqual(expected_faq, actual_faq)

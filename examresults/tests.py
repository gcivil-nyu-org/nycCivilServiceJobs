from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class ExamResultsDataTest(TestCase):
    def test_exam_results_page(self):
        response = self.client.get(reverse("examresults:exams"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "examresults/exams.html")

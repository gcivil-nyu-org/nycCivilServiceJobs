from django.test import TestCase
from django.urls import reverse
from examresults.models import ExamResultsActive
import json

# Create your tests here.


class ExamResultsDataTest(TestCase):
    def setUp(self):
        exam = ExamResultsActive(
            exam_number=1,
            list_number=1,
            first_name="first_name",
            last_name="last_name",
            middle_initial="middle",
            adjust_final_average=100.0,
            list_title_code="1234",
            list_title_desc="test_desc",
        )
        exam.save()

    def test_exam_results_page(self):
        response = self.client.get(reverse("examresults:exams"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "examresults/exams.html")

    def test_title_dropdown(self):
        response = self.client.get(reverse("examresults:exams"), {"q": "test"})
        title_desc = [
            x["list_title_desc"]
            for x in ExamResultsActive.objects.filter(list_title_desc__icontains="test")
            .values("list_title_desc")
            .distinct()
        ]
        self.assertEqual(title_desc, response.context["title_desc"])

        response = self.client.get(reverse("examresults:exams"), {"q": 1})
        title_desc = [
            x["list_title_desc"]
            for x in ExamResultsActive.objects.filter(list_title_desc__icontains="test")
            .values("list_title_desc")
            .distinct()
        ]
        self.assertEqual(title_desc, response.context["title_desc"])

    def test_exam_json_response(self):
        response = self.client.get(reverse("examresults:exams_data"))
        self.assertEqual(response.status_code, 200)

    def test_exam_json_data(self):
        response = self.client.get(reverse("examresults:exams_data"), {"q": 1123123123})

        self.assertEqual(json.loads(response.content)["recordsTotal"], 0)
        response = self.client.get(reverse("examresults:exams_data"), {"q": "test"})
        self.assertEqual(json.loads(response.content)["recordsTotal"], 1)

from django.test import TestCase
from sodapy import Socrata
from django.urls import reverse

client_socrata = Socrata(
    "data.cityofnewyork.us",
    "m7QHRP2U6tqRR7XCge8TzIRUW",
    username="nycCivilService.csgy6063@gmail.com",
    password="team4Pythonpir@tes",
    timeout=30,
)

# Create your tests here.


class JobDataTest(TestCase):
    # def setUp(self):
    #     self.totalJobsNYCOpenData=int(client_socrata.get("kpav-sd4t",
    #     select="COUNT(*)",where= "job_id is not null")[0]['COUNT'])
    # def test_match_job_count(self):
    #     jobs_db_count=job_record.objects.count()
    #     self.assertTrue(self.totalJobsNYCOpenData>1)

    def test_jobs_page(self):
        response = self.client.get(reverse("jobs:jobs"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "jobs/jobs.html")

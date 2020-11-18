from django.test import TestCase
from django.urls import reverse
from register.models import User
from jobs.models import UserSavedJob, job_record
from django.utils import timezone


class JobDataTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            is_hiring_manager="False",
            username="testjane",
            first_name="Jane",
            last_name="Doe",
            dob="1994-10-02",
            email="testjane@test.com",
            password="thisisapassword",
        )
        for i in range(10):
            job = job_record(
                job_id=i,
                agency="test_agency",
                posting_type="test_posting_type",
                num_positions=10,
                business_title="test_business_title",
                civil_service_title="test_civil_service_title",
                title_classification="test_title_classification",
                title_code_no="test_title_code_no",
                level="test_level",
                job_category="test_job_category",
                full_time_part_time_indicator="test_full_time",
                career_level="test_career_level",
                salary_range_from=100000,
                salary_range_to=120000,
                salary_frequency="test_salary_frequency",
                work_location="test_work_location",
                division_work_unit="test_division_work_unit",
                job_description="test_job_description",
                minimum_qual_requirements="test_minimum_qual_requirements",
                preferred_skills="test_preferred_skills",
                additional_information="test_additional_information",
                to_apply="test_to_apply",
                hours_shift="test_hours_shift",
                work_location_1="test_work_location_1",
                recruitment_contact="test_recruitment_contact",
                residency_requirement="test_residency_requirement",
                posting_date=timezone.now(),
                post_until=None,
                posting_updated=None,
                process_date=timezone.now(),
            )
            job.save()

    def test_home_page(self):
        # not logged in home returns landing page
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        # landing page shows correct jobs count from database
        self.assertEqual(response.context["total_jobs"], job_record.objects.count())

        # not logged in try accessing dashboard redirected to landing
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertRedirects(response, reverse("index"), fetch_redirect_response=False)
        # logged in home redirects to dashboard
        self.client.login(username=self.test_user.username, password="thisisapassword")
        response = self.client.get(reverse("index"))
        self.assertRedirects(
            response, reverse("dashboard:dashboard"), fetch_redirect_response=False
        )

    def test_saved_jobs_dashboard_page(self):
        # not logged in try accessing savedjobs page redirects landing
        response = self.client.get(reverse("dashboard:savedjobs"))
        self.assertRedirects(response, reverse("index"), fetch_redirect_response=False)
        # logged in accessing savedjobs displays saved jobs
        self.client.login(username=self.test_user.username, password="thisisapassword")
        response = self.client.get(reverse("dashboard:savedjobs"))
        self.assertTemplateUsed(response, "dashboard/savedjobs.html")

    def test_save_jobs_count_on_dashboard(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )

        self.client.post(
            reverse("jobs:saveJob", kwargs={"pk": job_record.objects.get(id=1).id})
        )
        self.assertTrue(user_login)
        saved_job_count = (
            UserSavedJob.objects.filter(user=self.test_user)
            .filter(job=job_record.objects.get(id=1))
            .count()
        )
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(len(response.context["saved_jobs_user"]), saved_job_count)

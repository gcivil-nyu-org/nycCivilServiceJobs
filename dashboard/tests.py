from django.test import TestCase
from django.urls import reverse
from register.models import User
from jobs.models import UserSavedJob, job_record
from dashboard.models import ExamSubscription
from examresults.models import CivilServicesTitle, ExamResultsActive
from django.db.models import Q
from django.utils import timezone
import datetime
import json


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

        # set up fake jobs
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

        # set up fake Civil Service title
        for i in range(15):
            civil_service_title = CivilServicesTitle(
                title_code=i + 1, title_description="title_description_" + str(i + 1)
            )
            civil_service_title.save()

        # set up fake Exam Reuslt Service title
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

    def test_home_page(self):
        # not logged in home returns landing page
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        # landing page shows correct jobs count from database
        expected_count = job_record.objects.filter(
            Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)
        ).count()
        self.assertEqual(response.context["total_jobs"], expected_count)

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

    def test_subscription_view(self):

        # not logged in try accessing subscription page redirects signin
        response = self.client.get(reverse("dashboard:subscription"))
        self.assertRedirects(
            response, reverse("signin:signin"), fetch_redirect_response=False
        )

        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.get(reverse("dashboard:subscription"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertTemplateUsed(response, "dashboard/subscription.html")

        expected_cst_qs = list(CivilServicesTitle.objects.all())
        actual_cst_qs = list(response.context["civil_services_title_all"])
        self.assertEqual(expected_cst_qs, actual_cst_qs)

        self.assertQuerysetEqual(
            response.context["user_subscribed_exams"],
            ExamSubscription.objects.filter(
                user=response.context["user"], is_notified=False
            ),
        )
        self.assertQuerysetEqual(
            response.context["user_subscribed_exam_results"],
            ExamSubscription.objects.filter(
                user=response.context["user"], is_notified=False
            ),
        )

    def test_save_subscription_upcoming_exam_view_user_not_logged_in_save(self):
        response = self.client.post(
            reverse("dashboard:SaveCivilServiceTitleView"),
            data={"civilservicetitleid": 1},
        )
        self.assertEqual(
            json.loads(response.content)["response_data"], "User not authenticated"
        )

    def test_save_subscription_upcoming_exam_view_user_logged_in_save(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("dashboard:SaveCivilServiceTitleView"),
            data={"civilservicetitleid": 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["response_data"], "CIVIL_SERVICE_TITLE_SAVED"
        )

        response = self.client.post(
            reverse("dashboard:SaveCivilServiceTitleView"),
            data={"civilservicetitleid": 1},
        )
        self.assertEqual(
            json.loads(response.content)["response_data"],
            "CIVIL_SERVICE_TITLE_ALREADY_PRESENT",
        )

    def test_delete_subscription_upcoming_exam_view_user_not_logged_in_save(self):
        response = self.client.post(
            reverse("dashboard:CivilServiceTitleDeleteView"),
            data={"civilservicetitleid": 1},
        )
        self.assertEqual(
            json.loads(response.content)["response_data"], "User not authenticated"
        )

    def test_delete_subscription_upcoming_exam_view_user_logged_in_save(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("dashboard:SaveCivilServiceTitleView"),
            data={"civilservicetitleid": 2},
        )

        # civilservicetitleid is the backend key(id) for the oject added in line 233
        response = self.client.post(
            reverse("dashboard:CivilServiceTitleDeleteView"),
            data={"civilservicetitleid": 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["response_data"], "CIVIL_SERVICE_TITLE_DELETED"
        )

    def test_save_subscription_upcoming_exam_result_view_user_not_logged_in_save(self):
        response = self.client.post(
            reverse("dashboard:SaveExamNumberView"), data={"examno": 5415}
        )
        self.assertEqual(
            json.loads(response.content)["response_data"], "User not authenticated"
        )

    def test_save_subscription_upcoming_exam_result_view_user_logged_in_save(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("dashboard:SaveExamNumberView"), data={"examno": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["response_data"], "EXAM_ALREADY_RELEASED"
        )
        response = self.client.post(
            reverse("dashboard:SaveExamNumberView"), data={"examno": 2}
        )
        self.assertEqual(json.loads(response.content)["response_data"], "EXAM_SAVED")

        response = self.client.post(
            reverse("dashboard:SaveExamNumberView"), data={"examno": 2}
        )
        self.assertEqual(
            json.loads(response.content)["response_data"], "EXAM_ALREADY_PRESENT"
        )

    def test_delete_subscription_upcoming_exam_result_view_user_not_logged_in_save(
        self,
    ):
        response = self.client.post(
            reverse("dashboard:ExamResultsDeleteView"), data={"examno": 1}
        )
        self.assertEqual(
            json.loads(response.content)["response_data"], "User not authenticated"
        )

    def test_delete_subscription_upcoming_exam_result_view_user_logged_in_save(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("dashboard:SaveExamNumberView"), data={"examno": 5410}
        )

        # examno here is the backend end key(id) for the object added in line 265

        response = self.client.post(
            reverse("dashboard:ExamResultsDeleteView"), data={"examno": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["response_data"], "EXAM_SUBSCRIBED_DELETED"
        )

    def test_recommended_jobs_dashboard_page(self):
        # not logged in try accessing recommended page redirects landing
        response = self.client.get(reverse("dashboard:recommendedjobs"))
        self.assertRedirects(response, reverse("index"), fetch_redirect_response=False)
        # logged in accessing savedjobs displays saved jobs
        self.client.login(username=self.test_user.username, password="thisisapassword")
        response = self.client.get(reverse("dashboard:recommendedjobs"))
        self.assertTemplateUsed(response, "dashboard/recommendedjobs.html")

    def test_recommended_jobs_view(self):

        # set up fake jobs
        for i in range(15):
            job = job_record(
                job_id=i,
                agency="test_agency",
                posting_type="External",
                num_positions=10,
                business_title="test_business_title",
                civil_service_title="title_description_" + str(i + 1),
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

        # Test-Check if user is authenticated
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)

        """ Expectation is  1 because saved Jobs  executes since preference is null(
         not yet set) """
        # response = self.client.post(
        #     reverse("jobs:saveJob", kwargs={"pk": job_record.objects.get(id=5).id})
        # )
        # self.assertEqual(json.loads(response.content)["response_data"], "Job Saved")
        # saved_job = (
        #     job_record.objects.filter(civil_service_title="title_description_4")
        #     .filter(
        #         Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)
        #     )
        #     .filter(posting_type__iexact="External")
        #     .distinct()
        #     .order_by("-posting_date")[:10]
        # )
        # print(saved_job.count())
        # response = self.client.get(reverse("dashboard:recommendedjobs"))
        # self.assertEqual(response.context["jobs"].count(), 1)

        # Test-Pass Title ID 1 as the one user is interested and
        # ID 2 as one user currently holds
        response = self.client.post(
            reverse("signin:SaveCivilServiceTitleView"),
            data={"user_int_cst[]": [1]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["response_data"], "CST_SAVED")

        response = self.client.get(reverse("dashboard:recommendedjobs"))

        self.assertEqual(response.context["jobs"].count(), 1)

        # # Test - If user can save a job and save job 3 as saved job for the user

        response = self.client.post(
            reverse("signin:SaveCivilServiceTitleView"),
            data={"user_int_cst[]": [1], "user_curr_cst[]": [2]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["response_data"], "CST_SAVED")

        response = self.client.get(reverse("dashboard:recommendedjobs"))

        # Expectation is 2 because we have 2 CSTs saved in preferences and
        # savedjobs CST will not be executed
        self.assertEqual(response.context["jobs"].count(), 2)

        # Testing when there are more than 10 Jobs matching the CSTs in preferences
        response = self.client.post(
            reverse("signin:SaveCivilServiceTitleView"),
            data={
                "user_int_cst[]": [1, 3, 4, 5, 6, 7, 8, 9],
                "user_curr_cst[]": [2, 11, 13, 12],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["response_data"], "CST_SAVED")

        response = self.client.get(reverse("dashboard:recommendedjobs"))
        self.assertEqual(response.context["jobs"].count(), 10)

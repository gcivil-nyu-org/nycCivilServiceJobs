import json
from django.contrib.messages.api import get_messages
from django.test import TestCase
from django.core import mail
from django.urls import reverse
from register.models import User
from signin.apps import SigninConfig
from examresults.models import CivilServicesTitle
from signin.models import UsersCivilServiceTitle


class SigninConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(SigninConfig.name, "signin")


class SigninTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "testuser",
            "password": "secret",
            "email": "testuser@test.com",
        }

        self.wrongUsername = {
            "username": "testuserWrong",
            "password": "secret",
            "email": "testuser@test.com",
        }

        self.wrongPassword = {
            "username": "testuser",
            "password": "wrong",
            "email": "testuser@test.com",
        }

        User.objects.create_user(**self.credentials)

    def test_get_sigin_page(self):
        response = self.client.get(reverse("signin:signin"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "signin/signin.html")

    def test_login(self):
        # send login data
        response = self.client.post(
            reverse("signin:signin"), self.credentials, follow=True
        )
        # should be logged in now
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertRedirects(
            response, reverse("dashboard:dashboard"), fetch_redirect_response=False
        )
        # check if redirects user to success page when already logged in
        response = self.client.get(reverse("signin:signin"))
        self.assertRedirects(
            response, reverse("dashboard:dashboard"), fetch_redirect_response=False
        )

    # def test_get_success_page(self):
    #     response = self.client.get(reverse("signin:success"))
    #     self.assertEqual(response.status_code, 200)
    # self.assertEqual(response.template_name[0], 'signin/success.html')

    def test_wrong_username(self):

        response = self.client.post(
            reverse("signin:signin"), self.wrongUsername, follow=True
        )
        self.assertFalse(
            response.context["user"] is not None
            and response.context["user"].is_authenticated
        )
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password.")
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid username or password.", messages)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"][0],
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive.",
        )

    def test_wrong_password(self):

        response = self.client.post(
            reverse("signin:signin"), self.wrongPassword, follow=True
        )
        self.assertFalse(
            response.context["user"] is not None
            and response.context["user"].is_authenticated
        )
        # self.assertContains(response,'Invalid username or password.')
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password.")


class PasswordResetTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "testuser",
            "password": "secret",
            "email": "testuser@test.com",
        }

        User.objects.create_user(**self.credentials)

    def test_a_get_password_reset_page(self):
        response = self.client.get(reverse("signin:password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "signin/password_reset.html")

    def test_b_send_password_reset_email(self):
        response = self.client.post(
            reverse("signin:password_reset"), {"email": self.credentials["email"]}
        )
        self.assertEqual(response.status_code, 302)
        # Response should redirect to success url
        self.assertEqual(response.url, reverse("signin:password_reset_done"))
        url = response.url
        # At this point the system will "send" us an email. We can "check" it thusly:
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Password reset on testserver")
        # The password reset email sent page should be displayed.
        response1 = self.client.get(url)
        self.assertEqual(response1.template_name[0], "signin/password_reset_sent.html")

    def test_c_password_reset(self):
        response = self.client.post(
            reverse("signin:password_reset"), {"email": self.credentials["email"]}
        )
        self.assertEqual(response.status_code, 302)
        token = response.context[0]["token"]
        uid = response.context[0]["uid"]
        # Now we can use the token to get the password change form
        response1 = self.client.get(
            reverse(
                "signin:password_reset_confirm", kwargs={"token": token, "uidb64": uid}
            )
        )
        self.assertEqual(response1.status_code, 302)
        # Get the redirect URL
        url_response1 = response1.url
        # set_trace()
        # Now we post to the url with our new password:
        response3 = self.client.post(
            url_response1,
            {"new_password1": "Fallnyucs@2019", "new_password2": "Fallnyucs@2019"},
        )
        self.assertEqual(response3.status_code, 302)
        # If success, we should get the reset complete URL
        url_response3 = response3.url
        response4 = self.client.get(url_response3)
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(
            response4.template_name[0], "signin/password_reset_complete.html"
        )

    def test_d_get_password_reset_complete_page(self):
        response = self.client.get(reverse("signin:password_reset_complete"))
        self.assertEqual(
            response.template_name[0], "signin/password_reset_complete.html"
        )


class UserProfileTest(TestCase):
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

        self.test_user_hm = User.objects.create_user(
            is_hiring_manager="True",
            username="testHM",
            first_name="Jane",
            last_name="Doe",
            dob="1994-10-02",
            email="testHM@test.gov",
            password="thisisapassword",
        )

    def test_user_profile_page_user_not_logged_in(self):
        response = self.client.get(reverse("userprofile"))
        self.assertRedirects(
            response, reverse("signin:signin"), fetch_redirect_response=False
        )

    def test_user_profile_page_user_logged_in(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.get(reverse("userprofile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signin/user_profile.html")
        form = response.context["form"]
        self.assertEqual(form.instance.username, "testjane")

    def test_user_profile_update_user_not_looged_in(self):
        response = self.client.post(
            reverse("userprofile"),
            data={"first_name": "Jane_updated", "last_name": "Doe_updated"},
        )
        self.assertRedirects(
            response, reverse("signin:signin"), fetch_redirect_response=False
        )

    def test_user_profile_update(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("userprofile"),
            data={"first_name": "Jane_updated", "last_name": "Doe_updated"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signin/user_profile.html")
        form = response.context["form"]
        self.assertEqual(form.instance.first_name, "Jane_updated")
        self.assertEqual(form.instance.last_name, "Doe_updated")

    def test_user_profile_update_form(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("userprofile"),
            data={
                "is_hiring_manager": "False",
                "username": "testjane",
                "first_name": "Jane_updated",
                "last_name": "Doe_updated",
                "dob": "01/10/1992",
                "email": "testjane@test.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Your profile was successfully updated", messages)

    def test_user_profile_update_form_invalid_email(self):
        self.test_user1 = User.objects.create_user(
            is_hiring_manager="False",
            username="testjohn",
            first_name="John",
            last_name="Doe",
            dob="1994-10-02",
            email="testjohn@test.com",
            password="thisisapassword",
        )

        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("userprofile"),
            data={
                "is_hiring_manager": "False",
                "username": "testjane",
                "first_name": "Jane_updated",
                "last_name": "Doe_updated",
                "dob": "01/10/1992",
                "email": "testjohn@test.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        form.has_error(
            "email",
            "This Email is already in use for some other account. "
            "Please use a different email address.",
        )

    def test_user_profile_update_form_invalid_email_hm(self):
        user_login = self.client.login(
            username=self.test_user_hm.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("userprofile"),
            data={
                "is_hiring_manager": True,
                "username": "testHM",
                "first_name": "Jane_updated",
                "last_name": "Doe_updated",
                "dob": "01/10/1992",
                "email": "testHM@test.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        form.has_error(
            "email",
            "This email is not a valid Email Address for Hiring Manager. "
            "Please use a different email address.",
        )


class UserPreferencesSaveTest(TestCase):
    def createCivilServiceTitle(self):
        civil_service_title = CivilServicesTitle(
            title_code=1, title_description="title_description"
        )
        civil_service_title_2 = CivilServicesTitle(
            title_code=2, title_description="title_description_2"
        )
        civil_service_title.save()
        civil_service_title_2.save()

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

        self.createCivilServiceTitle()

    def test_save_preferences_view(self):
        response = self.client.post(
            reverse("signin:SaveCivilServiceTitleView"), data={"user_int_cst[]": [1]}
        )
        self.assertEqual(response.status_code, 200)

    def test_save_preferences_user_not_logged_in_save(self):
        response = self.client.post(
            reverse("signin:SaveCivilServiceTitleView"), data={"user_int_cst[]": [1]}
        )
        self.assertEqual(
            json.loads(response.content)["response_data"], "User not authenticated"
        )

    def test_save_preferences_user_logged_in(self):
        user_login = self.client.login(
            username=self.test_user.username, password="thisisapassword"
        )
        self.assertTrue(user_login)
        response = self.client.post(
            reverse("signin:SaveCivilServiceTitleView"),
            data={"user_int_cst[]": [1], "user_curr_cst[]": [2]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["response_data"], "CST_SAVED")
        saved_cst_int_count = (
            UsersCivilServiceTitle.objects.filter(user=self.test_user)
            .filter(civil_service_title=CivilServicesTitle.objects.get(id=1))
            .filter(is_interested=True)
            .count()
        )
        saved_cst_curr_count = (
            UsersCivilServiceTitle.objects.filter(user=self.test_user)
            .filter(civil_service_title=CivilServicesTitle.objects.get(id=2))
            .filter(is_interested=False)
            .count()
        )
        self.assertEqual(saved_cst_int_count, 1)
        self.assertEqual(saved_cst_curr_count, 1)

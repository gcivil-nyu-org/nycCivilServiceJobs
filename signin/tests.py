from django.test import TestCase
from django.core import mail
from django.urls import reverse
from register.models import User
from signin.apps import SigninConfig


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
            response, reverse("signin:success"), fetch_redirect_response=False
        )

    def test_get_success_page(self):
        response = self.client.get(reverse("signin:success"))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.template_name[0], 'signin/success.html')

    def test_wrong_username(self):

        response = self.client.post(
            reverse("signin:signin"), self.wrongUsername, follow=True
        )
        self.assertFalse(
            response.context["user"] is not None
            and response.context["user"].is_authenticated
        )
        # set_trace()
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password.")
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
        # set_trace()
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

from django.test import TestCase, Client
from django.urls import reverse


class CustomErrorHandlerTests(TestCase):
    def test_handler_renders_template_response(self):

        response = self.client.get("/404/")
        self.assertEqual(response.context["code"], 404)
        self.assertTemplateUsed(response, "errors/errors.html")
        self.assertContains(response, "Nothing was found")

        response = self.client.get(reverse("signin:error403"))
        self.assertEqual(response.context["code"], 403)
        self.assertTemplateUsed(response, "errors/errors.html")
        self.assertContains(response, "Resource Forbidden")

        response = self.client.get(reverse("signin:error400"))
        self.assertEqual(response.context["code"], 400)
        self.assertContains(response, "")
        self.assertTemplateUsed(response, "errors/errors.html")

        c = Client(raise_request_exception=False)
        response = c.get(reverse("signin:error500"))
        self.assertEqual(response.context["code"], 500)
        self.assertContains(response, "There was error on our side")
        self.assertTemplateUsed(response, "errors/errors.html")

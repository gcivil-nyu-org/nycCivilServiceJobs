from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='test124test!', email='test@example.com')
        self.user.save()

    def test_correct(self):
        user = authenticate(username='testuser', password='test124test!')
        self.assertTrue(user is not None)
        self.assertTrue(user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='test124test!')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='testuser', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)



# Create your tests here.
from register.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from register.forms import *
from http import HTTPStatus


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register:signup')
        self.dummy_user = User.objects.create(is_hiring_manager = True, username = 'testjane',
                                               first_name ='Jane',last_name ='Doe',
                                               dob = '1994-10-02', email = 'janetest@username.gov',
                                               password = 'thisisapassword')
                
        self.user ={
            'is_hiring_manager': 'True',
            'username':'testuser',
            'first_name':'john',
            'last_name':'doe',
            'dob': '01/10/1992',
            'email': 'test@username.gov',
            'password1':'thisisapassword',
            'password2': 'thisisapassword',
        }
        self.user_no_username ={
            'is_hiring_manager': 'False',
            'username':'',
            'first_name':'john',
            'last_name':'doe',
            'dob': '01/10/1992',
            'email': 'test@username.gov',
            'password1':'thisisapassword',
            'password2': 'thisisapassword',
        }

        self.user_name_exists ={
            'is_hiring_manager': 'False',
            'username':'testjane',
            'first_name':'john',
            'last_name':'doe',
            'dob': '01/10/1992',
            'email': 'test@username.com',
            'password1':'thisisapassword',
            'password2': 'thisisapassword',
        }

        self.user_email_exists ={
            'is_hiring_manager': 'True',
            'username':'testjane',
            'first_name':'john',
            'last_name':'doe',
            'dob': '01/10/1992',
            'email': 'janetest@username.gov',
            'password1':'thisisapassword',
            'password2': 'thisisapassword',
        }


        self.user_hm_invalid_email ={
            'is_hiring_manager': 'True',
            'username':'testjane',
            'first_name':'john',
            'last_name':'doe',
            'dob': '01/10/1992',
            'email': 'jane@username.com',
            'password1':'thisisapassword',
            'password2': 'thisisapassword',
        }

        return super().setUp

class RegisterFormTest(BaseTest):
    
    def test_form_not_valid(self):
        form = SignUpForm(self.user_no_username)
        self.assertFalse(form.is_valid())
        
    def test_form_valid(self):
        form = SignUpForm(self.user)
        self.assertTrue(form.is_valid())

    def test_form_username_exists(self):
        form = SignUpForm(self.user_name_exists)
        form.has_error('username', 'A user with that username already exists.')

    def test_form_email_exists(self):
        form = SignUpForm(self.user_email_exists)
        form.has_error('email', 'This Email is already registered. Please use a different email address.')

    def test_form_hm_invalid_email(self):
        form = SignUpForm(self.user_hm_invalid_email)
        form.has_error('This email is not a valid Email Address for Hiring Manager. Please use a different email address.')


class RegisterTest(BaseTest):
    
    # Setup for the test    
    def test_can_view_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'register/signup.html')


    def test_user_can_register_as_HM(self):
        user_count = User.objects.count()
        response = self.client.post(self.register_url,self.user, format='text/html')
        user_count = user_count+1
        self.assertEqual(User.objects.count(), user_count)
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed(response,'register/account_activated.html')
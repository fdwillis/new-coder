import ecom_project.settings as settings
from django.shortcuts import render_to_response
from django.test import TestCase, RequestFactory
from django.db import IntegrityError
from django import forms
from .models import User
from .forms import SigninForm, UserForm
from .views import soon, register
from django.core.urlresolvers import resolve
from pprint import pformat
from main.factories import *
import unittest
import mock

class UserModelTest(TestCase):
	@classmethod
	def setUp(klass):
		klass.test_user = User(email = 'test@t.com', name = "test")
		klass.test_user.save()

	def test_users_email_prints(self):
		self.assertEquals(str(self.test_user), "test@t.com")

	def test_get_by_id(self):
		self.assertEquals(User.get_by_id(1), self.test_user)

class FormTesterMixin():
	def assertFormError(self, form_klass, expected_error_name, expected_error_msg, data):
		test_form = form_klass(data = data)

		# dont validate form with errors
		self.assertFalse(test_form.is_valid())

		self.assertEquals(
			test_form.errors[expected_error_name], 
			expected_error_msg,
			msg = "Expected {} : Actual {} : using data {}".format(
				test_form.errors[expected_error_name], 
				expected_error_msg, pformat(data)
			)
		)

class FormTests(unittest.TestCase, FormTesterMixin):

	def test_signin_validation_for_invalid_data(self):
		invalid_data_list = [
			{'data': 
				{'email': 'j@j.com'},
				'error': ('password', [u'This field is required.'])
			},
			{'data':
				{'password': '1234'},
				'error': ('email', [u'This field is required.'])
			}
		]

		for invalid_data in invalid_data_list:
			self.assertFormError(SigninForm, 
													 invalid_data['error'][0], 
													 invalid_data['error'][1], 
													 invalid_data["data"])


	def test_user_form_passwords_match(self):
		form = UserForm(
			{
				'name': 'asd',
				'email': 'asdf@g.com', 
				'password': "user.password",
				'ver_password': "user.password",
				'last_4_digits': "3434",
				'stripe_token': "2"
			}
		)

		# If data not valid print the errors
		self.assertTrue(form.is_valid(), form.errors)

		# Error if form isnt cleaned correctly
		self.assertIsNotNone(form.clean())

	def test_user_form_passwords_dont_match_throws_error(self):
		form = UserForm(
			{
				'name': 'sdfk',
				'email': "sdfk@g.com", 
				'password': "342",
				'ver_password': '43983',
				'last_4_digits': "3434",
				'stripe_token': "1"
			}
		)

class ViewTesterMixin(object):

    @classmethod
    def setupViewTester(klass, url, view_func, expected_html,
                        status_code=200,
                        session={}):
        request_factory = RequestFactory()
        klass.request = request_factory.get(url)
        klass.request.session = session
        klass.status_code = status_code
        klass.url = url
        klass.view_func = staticmethod(view_func)
        klass.expected_html = expected_html

    def test_resolves_to_correct_view(self):
        test_view = resolve(self.url)
        self.assertEquals(test_view.func, self.view_func)

    def test_returns_appropriate_respose_code(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.content, self.expected_html)

class RegisterPageTests(TestCase, ViewTesterMixin):
	@classmethod
	def setUpClass(klass):
		html = render_to_response(
			'register.html', 
			{
				'form': UserForm(),
				'months': range(1,12),
				'publishable': settings.STRIPE_PUBLISHABLE,
				'soon': soon,
				'user': None, 
				'years': range(2011, 2036),
			}
		)

		ViewTesterMixin.setupViewTester(
			'/register', 
			register, 
			html.content, 
		)

	def setUp(self):
		request_factory = RequestFactory()
		self.request = request_factory.get(self.url)

	def test_invalid_form_returns_regis_page(self):
		with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
			user_mock.return_value = False

			self.request.method = "POST"
			self.request.POST = None

			#grab register page
			resp = register(self.request)

			# current page equals register page
			self.assertEquals(resp.content, self.expected_html)

			# was the is_valid method called?
			self.assertEquals(user_mock.call_count, 1)

	def test_new_user_signup_is_success(self):
		self.request.session = {}
		self.request.method = 'POST'
		self.request.POST = {
			'email': 'python@t.com', 
			'name': 'New User Test', 
			'stripe_token': '4242424242424242', 
			'last_4_digits': '4242',
			'password': 'password', 
			'ver_password': 'password',
		}
		with mock.patch('stripe.Customer') as stripe_mock:
			config = {"create.return_value": mock.Mock()}
			stripe_mock.configure_mock(**config)

			resp = register(self.request)
			self.assertEquals(resp.content, "")
			self.assertEquals(resp.status_code, 302)
			self.assertEquals(self.request.session['user'], 1)

			# throws error if user not in DB
			User.objects.get(email="python@t.com")

	def test_registering_user_twice_gives_error(self):

		# create user with same email to get error
		user = User(name='same user', email="python@t.com")
		user.save()

		# create the request used to ttest the view
		self.request.session = {}
		self.request.method = 'POST'
		self.request.POST = {
			'email': 'python@t.com', 
			'name': 'pyth', 
			'stripe_token': '4242424242424242',
			'last_4_digits': '4242',
			'password': 'password', 
			'ver_password': 'password',
		}

		# create expected form
		expected_form = UserForm(self.request.POST)
		expected_form.is_valid()
		expected_form.addError('python@t.com is already a member')

		# create the expected html
		html = render_to_response(
			'register.html', 
			{
				'form': expected_form, 
				'months': range(1,12), 
				'publishable': 'STRIPE_PUBLISHABLE', 
				'soon': soon(),
				'user': None, 
				'years': range(2011, 2036),
			}
		)

		# mock out stripe so we dont hit their server
		with mock.patch('stripe.Customer') as stripe_mock:
			config = {"create.return_value": mock.Mock()}
			stripe_mock.configure_mock(**config)

			#run test
			resp = register(self.request)

			# verify things were done correctly
			self.assertEquals(resp.status_code, 200)
			self.assertEquals(self.request.session, {})
			self.assertEquals(resp.content, html.content)

			# assert only one record in DB
			users = User.objects.filter(email = 'python@t.com')
			self.assertEquals(len(users), 1)







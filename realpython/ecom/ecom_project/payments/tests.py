from django.test import TestCase
from payments.models import User
from payments.forms import SigninForm
from pprint import pformat
import unittest

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








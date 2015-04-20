"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index
from django.shortcuts import render_to_response
import mock
from main.factories import *
from payments.models import User
from django.test import RequestFactory



class MainPageTests(TestCase):

	##############
	### Set Up ###
	##############

	@classmethod
	def setUp(klass):
		request_factory = RequestFactory()
		klass.request = request_factory.get("/")
		klass.request.session = {}

	###################
	### Test Routes ###
	###################

	def test_roots_to_main_view(self):
		main_page = resolve('/')
		self.assertEqual(main_page.func, index)

	def test_returns_response_code(self):
		resp = index(self.request)
		self.assertEquals(resp.status_code, 200)

	#############################
	### Test Template & Views ###
	#############################

	def test_returns_exact_html(self):
		resp = index(self.request)
		self.assertEquals(
			resp.content, 
			render_to_response('index.html').content
		)

	def test_loggedin_user(self):
		#make a user
		user = UserFactory()
		user_id = user.id
		print user_id
		
		request_factory = RequestFactory()
		request = request_factory.get('/')

		# Create session with a user
		request.session = { 'user': str(user_id) }

		# grab index page
		resp = index(request)

		# verify returns page for logged in user
		expectedHtml = render_to_response(
			'user.html', { 'user': user })
		self.assertEquals(resp.content, expectedHtml.content)
		
		#reset session
		request.session = {}










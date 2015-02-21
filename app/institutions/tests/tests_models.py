"""This function makes tests to the views"""
import unittest

from django.test import Client


class SignUpTest(unittest.TestCase):
    def setUp(self):
        """initialize a client (meaning a browser) and visits the page"""
        self.client = Client()

    def test_access(self):
        # create a get request
        response = self.client.get('/signup/')


        #check that the response is 220 ok
        self.assertEqual(response.status_code, 200)

    def test_dashboard_not_signed(self):
        """Test if the browser redirects the login_required protected views"""
        views_url = ('/dashboard/',
                     '/create_event/',
                     '/accounts/password_change/',
                    '/accounts/picture/')

        #create a get request
        for view in views_url:
             response = self.client.get(view)
             #the user was not logged in, the user should be redirected
             self.assertEqual(response.status_code, 302,
                     msg=str(response.request))


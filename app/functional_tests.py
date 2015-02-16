"""This file contains all the text related to how
the website should work."""
import unittest
from selenium import webdriver

class NewUserTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_starting_login(self):
        self.browser.get('http://localhost:8001')
        self.assertIn( 'Red Nacional de Emprendimiento', browser.title)



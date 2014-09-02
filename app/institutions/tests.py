from django.test import TestCase
from .context import UserAdministrationContext
from .models import UserProfile

class UserAdministrationTestCase(TestCase):

	def setUp(self):
		self.user_administration_context = UserAdministrationContext()
	
	def test_administrator_add_approval_to_user(self):

		user = UserProfile()
		
		self.assertEqual(user.approved, False)
		self.user_administration_context.approve(user)		
		self.assertEqual(user.approved, True)

	def test_administrator_remove_approval_to_user(self):
		user = UserProfile()

		self.user_administration_context.approve(user)
		self.assertEqual(user.approved, True)
		self.user_administration_context.unapprove(user)

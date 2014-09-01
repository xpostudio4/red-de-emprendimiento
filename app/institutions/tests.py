from django.test import TestCase
from institutions.models import UserProfile

class UserAdministrationTestCase(TestCase):

	def setUp(self):
		self.user_administration_context = UserAdministrationContext()
	
	def test_user_add_administrator_approval(self):

		user = UserProfile()
		
		self.assertEqual(user.approved, False)
		self.user_administration_context.approve(user)		
		self.assertEqual(u.approved, True)

	def test_user_remove_administration_approval(self):
		user = UserProfile()

		self.user_administration_context.approved(user)
		self.assertEqual(user.approved, True)
		user_administration_context.unapprove(user)

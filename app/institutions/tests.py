from django.test import TestCase
from institutions import User

class UserTestCase(TestCase):
	def test_user_needs_administrator_approval(self):
		user = User()
		user_administration_context = UserAdministrationContext()
		user_administration_context.approve(user)		
		self.assertEqual(u.approved, True)

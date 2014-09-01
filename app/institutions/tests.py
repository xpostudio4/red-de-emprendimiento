from django.test import TestCase
from institutions import User

class UserAdministrationTestCase(TestCase):

	def setUp(self):
		user_administration_context = UserAdministrationContext()
	
	def test_user_add_administrator_approval(self):
	
		user = User()
		
		self.assertEqual(user.approved, False)
		user_administration_context.approve(user)		
		self.assertEqual(u.approved, True)

	def test_user_remove_administration_approval(self):
		user = User()

		user_administration_context.approved(user)
		self.assertEqual(user.approved, True)
		user_administration_context.unapprove(user)

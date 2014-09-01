from django.test import TestCase

class UserAdministrationTestCase(TestCase):

	def setUp(self):
		self.user_administration_context = UserAdministrationContext()
	
	def test_administrator_add_approval_to_user(self):

		user = User()
		
		self.assertEqual(user.approved, False)
		self.user_administration_context.approve(user)		
		self.assertEqual(u.approved, True)

	def test_administrator_remove_approval_to_user(self):
		user = User()

		self.user_administration_context.approved(user)
		self.assertEqual(user.approved, True)
		user_administration_context.unapprove(user)

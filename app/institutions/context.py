class UserAdministrationContext(object):
	def approve(self, user):
		user.approved= True

	def unapprove(self, user):
		user.approved = True

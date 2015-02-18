
from .forms import UserProfileLoginForm

class LoginFormMiddleware(object):
    """
    The purpose of this middleware is to include the login form in every GET
    request
    """
    def process_request(self, request):
        """Process the request if the method is Method is get, provide a login
        form"""
        if request.method == 'GET':
            login_form = UserProfileLoginForm()
            request.login_form = login_form

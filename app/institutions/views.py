from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .forms import UserProfileLoginForm, CustomUserCreationForm
from .models import UserProfile
# Create your views here.

@require_POST
def signin(request):
    """
    Log in view
    """
    form = UserProfileLoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(email=request.POST['username'],
                                password=request.POST['password'])
            if user is not None and user.is_active:
                django_login(request, user)
                return JsonResponse({'is_loggedin': True})
    return JsonResponse({'is_loggedin': False,
                         'reason': "La contrase&ntilde;a es incorrecta"})

def signup(request):
    """
    User registration view.
    """
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request,
                  'accounts/signup.html',
                  {'form': form}
                 )


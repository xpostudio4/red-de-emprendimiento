from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
from .forms import UserProfileLoginForm, CustomUserCreationForm, OrganizationForm
from .models import UserProfile
import datetime
# Create your views here.

@require_POST
def signin(request):
    """
    Log in view
    """
    form = UserProfileLoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(email=request.POST['username'], password=request.POST['password'])
            if user is not None and user.is_active:
                    django_login(request, user)
                    return JsonResponse({'is_loggedin': True})
    return JsonResponse({'is_loggedin': False,
                         'reason': "La contrase&ntilde;a es incorrecta"})

def signup(request):
    """
    User registration view.
    """
    user_form = CustomUserCreationForm(request.POST or None)
    organization_form = OrganizationForm(request.POST or None)
    if request.method == 'POST':

        if user_form.is_valid() and organization_form.is_valid():
            organization = organization_form.save()
            user = user_form.save(commit=False) 
            user.organization = organization
            user.save()
            return HttpResponseRedirect('/')
    else:
        return render_to_response(
                'accounts/signup.html', {'user_form': user_form, 'organization_form': organization_form},
                context_instance=RequestContext(request)
                )
    return render_to_response('accounts/signup.html',
            { 'user_form': user_form, 'errors': form.errors, 'organization_form': organization_form},
                context_instance=RequestContext(request))


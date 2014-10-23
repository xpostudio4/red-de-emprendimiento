from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from .forms import UserProfileLoginForm, CustomUserCreationForm
from .models import UserProfile
import datetime
# Create your views here.

def signin(request):
    """
    Log in view
    """
    if request.method == 'POST':
        form = UserProfileLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['username'], password=request.POST['password'])
            if user is not None and user.is_active:
                    django_login(request, user)
                    return redirect('/dashboard')
    else:
       form = UserProfileLoginForm()
    return render_to_response('accounts/signin.html',
            {'form': form, 'form_errors': form.errors,},
           context_instance=RequestContext(request))


def signup(request):
    """
    User registration view.
    """
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            user = form.save()
            return redirect('/accounts/signin')

    else:
        return render_to_response(
                'accounts/signup.html', {'form': form},
                context_instance=RequestContext(request)
                )
    return render_to_response('accounts/signup.html',
            { 'form': form, 'errors': form.errors},
                context_instance=RequestContext(request))


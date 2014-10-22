from django import forms
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from institutions.forms import OrganizationForm, EventForm,UserProfileChangeForm

def home(request):
    return render(request, 'site/index.html')

def inspire(request):
    return render(request, 'site/inspira.html')

# @login_required
def dashboard(request):
	organization_form = OrganizationForm()
	event_form = EventForm()
	user_form = UserProfileChangeForm()
    	return render(request, 'site/dashboard.html',
            {'organization_form': organization_form, 'event_form': event_form, 'user_form': user_form})


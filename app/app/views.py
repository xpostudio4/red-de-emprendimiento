from django import forms
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from institutions.forms import OrganizationForm, EventForm,UserProfileChangeForm
from institutions.models import UserProfile

def home(request):
    return render(request, 'site/index.html')

def inspire(request):
    return render(request, 'site/inspira.html')

@login_required
def dashboard(request):
    user = UserProfile(id=request.user.id)
    organization_form = OrganizationForm(instance=request.user.organization)
    event_form = EventForm()
    return render(request, 'site/dashboard.html',
            {'organization_form': organization_form, 'event_form': event_form})


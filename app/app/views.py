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
    #Load the forms with data or the instance of the file if POST
    if request.method == 'POST':
        organization_form = OrganizationForm(request.POST, instance=request.user.organization)
        event_form = EventForm(request.POST)
        user_form = UserProfileChangeForm(request.POST, instance=user)

        if organization_form.is_valid():
            organization_form.save()

    else:
        user_form = UserProfileChangeForm(instance=user)
        organization_form = OrganizationForm(instance=request.user.organization)
        event_form = EventForm()
    #process the forms if valid
    #Otherwise return the errors
    return render(request, 'site/dashboard.html',
            {'organization_form': organization_form, 'event_form': event_form})


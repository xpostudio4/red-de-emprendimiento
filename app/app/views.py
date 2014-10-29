import json
from django import forms
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from institutions.forms import OrganizationForm, EventForm,UserProfileChangeForm
from institutions.models import Event, Organization, UserProfile

def home(request):
    return render(request, 'site/index.html')

def inspire(request):
    return render(request, 'site/inspira.html')

@login_required
def dashboard(request):
    user = UserProfile(id=request.user.id)
    events = Event.objects.filter(organization=request.user.organization)
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
            {
                'organization_form': organization_form,
                'event_form': event_form,
                'events': events,
                })

@login_required
@require_POST
def event_creation(request,organization_id):
    #fill the form
    organization = Organization.objects.get(id=organization_id)
    form = EventForm(request.POST)
    #process and save
    if form.is_valid():
        event = form.save(commit=False)
        event.organization = organization
        event.save()
        #return the Json of the data
        result = {
                'name': event.name,
                'description': event.description,
                'from': str(event.from_date),
                'to': str(event.to_date)
                }
        return HttpResponse(json.dumps(result))
    return HttpResponse(json.dumps(form.errors))

@login_required
@require_POST
def event_deletion(request, event_id):
    #verify the user organization belongs 
    #deletes the item with the ID provided
    Event.objects.get(id=event_id, organization=request.user.organization).delete()
    return HttpResponse("The item has been deleted")

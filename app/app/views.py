import json
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.views.decorators.http import require_POST
from institutions.forms import OrganizationForm, EventForm,UserProfileChangeForm
from institutions.models import Event, Organization, UserProfile

def index(request):
    """
    The Index is where most of the action in the page will happen,
    the entrepreneurs should access this page and see all the opportunities
    available for them here.
    """
    return render(request, 'site/index.html')

def home(request):
    """
    The home shows the different options that the user can have, if the user
    is an entrepreneur they can choose all the options available in index.
    If the user belong to the support industry he can choose otherwise.
    """
    return render(request, 'home.html')

def inspire(request):
    return render(request, 'site/inspira.html')

@login_required
def dashboard(request):
    user_form = UserProfileChangeForm(request.POST or None, instance=request.user)
    events = Event.objects.filter(organization=request.user.organization)
    event_form = EventForm(request.POST or None)
    organization_form = OrganizationForm(request.POST or None, instance=request.user.organization)
        #Load the forms with data or the instance of the file if POST
    if request.method == 'POST':
            organization_form = OrganizationForm(request.POST, instance=request.user.organization)
            event_form = EventForm(request.POST)

            if organization_form.is_valid():
                organization_form.save()
    else:
        organization_form = OrganizationForm(instance=request.user.organization)
        event_form = EventForm()
        user_form = UserProfileChangeForm(instance=request.user)
    #process the forms if valid
    #Otherwise return the errors
    return render(request, 'site/dashboard.html',
            {
                'organization_form': organization_form,
                'event_form': event_form,
                'user_form': user_form,
                'events': events,
                })
@login_required
@require_POST
def user_validation(request):
    user_form = UserProfileChangeForm(request.POST, instance=request.user)
    if user_form.is_valid():
        user_form.save()
        return HttpResponseRedirect('/dashboard/')
    else:
        organization_form = OrganizationForm(instance=request.user.organization)
        event_form = EventForm()
        events = Event.objects.filter(organization=request.user.organization)
        return render(request, 'site/dashboard.html',
            {
                'organization_form': organization_form,
                'event_form': event_form,
                'user_form': user_form,
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
        #Get the date formats
        from_date = DateFormat(event.from_date)
        to_date = DateFormat(event.to_date)
        #return the Json of the data
        result = {
                'id' : event.id,
                'name': event.name,
                'description': event.description,
                'from': str(from_date.format(get_format('DATE_FORMAT'))),
                'to': str(to_date.format(get_format('DATE_FORMAT')))
                }
        return HttpResponse(json.dumps(result), content_type='application/json')
    return HttpResponse(json.dumps(form.errors))

@login_required
def event_deletion(request, event_id):
    #verify the user organization belongs 
    #deletes the item with the ID provided
    Event.objects.get(id=event_id, organization=request.user.organization).delete()
    return HttpResponse("The item has been deleted")

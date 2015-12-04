import datetime
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.views.decorators.http import require_POST
from institutions.models import Event, Organization, UserProfile
from institutions.forms import (DashboardUserCreationForm, OrganizationForm,
                                EventForm, OrganizationPictureForm,
                                UserProfileChangeForm)
from .functions import paginated_list


def about(request):
    return render(request, 'site/about.html')

def calendar(request):
    """General calendar view, here should be shown all the events"""
    events = paginated_list(request, Event, 20, 'from_date',
                            from_date__gte=datetime.date.today,
                            organization__is_active=True)
    
    past_events = paginated_list(request, Event, 20, 'from_date',
                            from_date__lt=datetime.date.today,
                            organization__is_active=True)
    return render(request, 'site/calendar.html', {'events': events, 'past_events': past_events})


def category(request, category_name):
    """
    The purpose of this page is to display all the organizations that have
    an specific  tag in their tag list.
    """
    organizations = paginated_list(request, Organization, 20, None,
                                   categories__name=category_name.capitalize(),
                                   is_active=True)
    return render(request, 'site/list.html',
                  {'organizations' : organizations})


@login_required
def dashboard(request):
    """User and organization edit board, here events are created"""
    user_form = UserProfileChangeForm(request.POST or None,
                                      instance=request.user)
    event_form = EventForm()
    events = Event.objects.filter(organization=request.user.organization).order_by('-from_date')
    new_orgs = Organization.objects.filter(is_active=False)
    new_user_form = DashboardUserCreationForm()
    organization = Organization.objects.get(id=request.user.organization.id)
    organization_form = OrganizationForm(request.POST or None,
                                         instance=organization)
    organization_picture_form = OrganizationPictureForm(request.POST or None,
                                                        instance=organization)
    password_form = SetPasswordForm(user=request.user)
    org_users = UserProfile.objects.filter(~Q(id=request.user.id),
                                           organization=request.user.organization)
    #Load the forms with data or the instance of the file if POST
    if request.method == 'POST':
        organization_form = OrganizationForm(request.POST,
                                             instance=request.user.organization)
        if organization_form.is_valid():
            organization = organization_form.save()
    else:
        organization_form = OrganizationForm(instance=request.user.organization)
        user_form = UserProfileChangeForm(instance=request.user)
    return render(request, 'site/dashboard.html',
                  {'events': events,
                   'event_form': event_form,
                   'new_orgs': new_orgs,
                   'new_user_form': new_user_form,
                   'organization': organization,
                   'organization_form': organization_form,
                   'organization_picture_form': organization_picture_form,
                   'org_users': org_users,
                   'password_form': password_form,
                   'user_form': user_form,
                  }
                 )


def events_view(request, category_name):
    """
    This view show all the events based on the category they belong to.
    """
    events = paginated_list(request, Event, 20, 'from_date',
                            from_date__gte=datetime.date.today,
                            categories__name=category_name)
    return render(request, 'site/list.html',
                  {'events' : events})


@login_required
@require_POST
def event_creation(request, organization_id):
    """Process the creation of events"""
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
    """Deletes the event through an Ajax request"""
    #verify the user organization belongs
    #deletes the item with the ID provided
    Event.objects.get(id=event_id, organization=request.user.organization).delete()
    return HttpResponse("The item has been deleted")


def index(request):
    """
    The index is where most of the action in the page will happen,
    the entrepreneurs should access this page and see all the opportunities
    available for them here.
    """
    return render(request, 'site/index.html')


@login_required
@require_POST
def picture_update(request):
    """The purpose of this view is to handle the upload of pictures
    from the dashboard and the returning of info to the dashboard"""
    #(we need to verify the user is logged in)
    if request.user.is_authenticated():
        #receive all the form information in a post request
        form = OrganizationPictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data['picture']
            organization = Organization.objects.get(id=request.user.organization.id)
            organization.logo = picture
            organization.save()
    return HttpResponseRedirect('/dashboard/')


def profile(request, slug):
    """"Organization profile is displayed here"""
    organization = get_object_or_404(Organization, slug=slug, is_active=True)
    profile = UserProfile.objects.filter(organization=organization)[0]
    events = Event.objects.filter(organization=organization).order_by('-from_date')
    return render(request, 'site/profile.html', {'organization': organization,
                                                 'profile': profile,
                                                 'events':events})



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
                      {'organization_form': organization_form,
                       'event_form': event_form,
                       'user_form': user_form,
                       'events': events,
                      })

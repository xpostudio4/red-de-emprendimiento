import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.views.decorators.http import require_POST
from institutions.forms import OrganizationForm, EventForm,UserProfileChangeForm, OrganizationPictureForm
from institutions.models import Event, Organization, UserProfile


def calendar(request):
    """General calendar view, here should be shown all the events"""
    return render(request, 'site/calendar.html')


def capital(request):
    """
    The purpose of this page is to display all the organizations that have
    'inspire' tag in their tag list.
    """
    organizations = Organization.objects.filter(categories__name="Capital",
                                                is_active=True)
    return render(request, 'site/list.html',
                  {'organizations' : organizations})


def connect(request):
    """
    The purpose of this page is to display all the organizations that have
    'inspire' tag in their tag list.
    """
    organizations = Organization.objects.filter(categories__name="Conecta",
                                                is_active=True)
    return render(request, 'site/list.html',
                  {'organizations' : organizations})


def create(request):
    """
    The purpose of this page is to display all the organizations that have
    'inspire' tag in their tag list.
    """
    organizations = Organization.objects.filter(categories__name="Crea",
                                                is_active=True)
    return render(request, 'site/list.html',
                  {'organizations' : organizations})


@login_required
def dashboard(request):
    """User and organization edit board, here events are created"""
    user_form = UserProfileChangeForm(request.POST or None,
                                      instance=request.user
                                     )
    user = UserProfile.objects.get(id=request.user.id)
    organization = Organization.objects.get(id=request.user.organization.id)
    events = Event.objects.filter(organization=user.organization).order_by('-from_date')
    event_form = EventForm()
    organization_form = OrganizationForm(request.POST or None,
                                         instance=organization
                                        )
    organization_picture_form = OrganizationPictureForm(request.POST or None,
                                                        instance=organization
                                                       )
        #Load the forms with data or the instance of the file if POST
    if request.method == 'POST':
        organization_form = OrganizationForm(request.POST,
                                             instance=request.user.organization
                                            )
        if organization_form.is_valid():
            organization = organization_form.save()
    else:
        organization_form = OrganizationForm(instance=request.user.organization)
        user_form = UserProfileChangeForm(instance=request.user)
        print organization_form
    return render(request, 'site/dashboard.html',
                  {'organization': organization,
                   'organization_form': organization_form,
                   'organization_picture_form': organization_picture_form,
                   'event_form': event_form,
                   'user_form': user_form,
                   'events': events,
                  }
                 )


def guide(request):
    """
    The purpose of this page is to display all the organizations that have
    'inspire' tag in their tag list.
    """
    organizations = Organization.objects.filter(categories__name="Guia",
                                                is_active=True)
    return render(request, 'site/list.html',
                  {'organizations' : organizations})


def index(request):
    """
    The Index is where most of the action in the page will happen,
    the entrepreneurs should access this page and see all the opportunities
    available for them here.
    """
    return render(request, 'site/index.html')


def inspire(request):
    """
    The purpose of this page is to display all the organizations that have
    'inspire' tag in their tag list.
    """
    organizations = Organization.objects.filter(categories__name="Inspira",
                                                is_active=True)
    return render(request, 'site/list.html',
                  {'organizations' : organizations})


def profile(request, slug):
    """"Organization profile is displayed here"""
    organization = get_object_or_404(Organization, slug=slug, is_active=True)
    profile = UserProfile.objects.get(organization=organization)
    events = Event.objects.filter(organization=organization).order_by('-from_date')
    return render(request, 'site/profile.html', {'organization': organization,
                                                 'profile': profile, 
                                                 'events':events})


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
        else:
            print form.errors
    else:
        return HttpResponseForbidden()


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

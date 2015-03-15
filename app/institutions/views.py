from django.contrib.auth import (login as django_login, authenticate,
                                 logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Event, Organization
from .forms import (CustomUserCreationForm,
                    DashboardUserCreationForm,
                    EventForm, OrganizationForm,
                    UserProfileLoginForm)

@require_POST
@login_required
def approve_organization(request, organization_id):
    """This function responde to an ajax request asking to approve an
    organization"""
    if request.user.is_admin:
        organization = Organization.objects.get(id=organization_id)
        organization.is_active = True
        organization.save()
        return JsonResponse({'is_approved': True})
    return JsonResponse({'is_approved': False,
                         'reason': 'Solo los administradores pueden aprobar'})


@require_POST
@login_required
def create_event(request):
    """This view creates a new event from a registered organization,
    it returns Json"""
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.organization = request.user.organization
        event.save()
        form.save_m2m()
    return HttpResponseRedirect('/dashboard/')


@require_POST
@login_required
def dashboard_usercreation(request):
    """
    This view helps to create a new user of the
    person belonging to the organization.
    """
    user_form = DashboardUserCreationForm(request.POST or None)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.organization = request.user.organization
        new_user.save()
    return HttpResponseRedirect('/dashboard/')
        


@require_POST
@login_required
def delete_event(request, event_id):
    """
    This view deletes the event after receiving a POST request.
    """
    event = get_object_or_404(Event, id=event_id)
    if request.user.organization == event.organization:
        event.delete()
        return JsonResponse({"is_deleted": True})
    return JsonResponse({"is_deleted": False})


@require_POST
@login_required
def password_change(request):
    """This view process the password change of the user, returns Json"""
    password_form = SetPasswordForm(request.user, request.POST or None)
    #if form is valid
    if password_form.is_valid():
        #process the form by saving
        password_form.save()
        return JsonResponse({'is_changed': True})
    else:
        #else return the error as ajax
        print password_form.errors
        return JsonResponse({'is_changed': False,
                             'reasons': str(password_form.errors)})

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
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    user_form = CustomUserCreationForm(request.POST or None)
    organization_form = OrganizationForm(request.POST or None)
    if request.method == 'POST':
        if user_form.is_valid() and organization_form.is_valid():
            organization = organization_form.save()
            user = user_form.save(commit=False)
            user.is_admin = False
            user.organization = organization
            user.save()

            return HttpResponseRedirect('/')
    return render(request,
                  'accounts/signup.html',
                  {'user_form': user_form,
                   'organization_form': organization_form},
                 )


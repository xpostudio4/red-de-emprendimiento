from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.auth.decorators import login_required

def home(request):
    return render(request, 'site/index.html')

def inspire(request):
    return render(request, 'site/inspira.html')

@login_required
def dashboard(request):
    return render(request, 'site/dashboard.html')



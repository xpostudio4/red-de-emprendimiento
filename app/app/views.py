from django.shortcuts import render


def home(request):
    return render(request, 'site/index.html')

def inspire(request):
    return render(request, 'site/inspira.html')

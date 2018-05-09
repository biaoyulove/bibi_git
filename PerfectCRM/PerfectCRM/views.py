from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect


def accounts_login(request):
    errors = {}
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user, password=password)
        if user:
            login(request, user)
            text_url = request.GET.get('next', '/')
            return HttpResponseRedirect(text_url)
        else:
            errors['error'] = 'Wrong username or password!'
    return render(request, "login.html", {'errors': errors})


def accounts_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

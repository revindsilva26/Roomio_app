from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html', {})


def logout_user(request):
    pass

def register_user(request):
    return render(request, 'register.html',{})
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("This is the authentication index")

def signUp(request):

    if request.method == 'GET':
        print("SIGN_UP GET")
        context = {}
        return render(request, 'authentication/signUp.html', context)
    elif request.method == 'POST':
        #user = User.objects.create_user('','','')

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username,email,password)

        context = {}

        return render(request, 'authentication/login.html', context)

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def index(request):
    return HttpResponse("This is the authentication index")

@csrf_exempt
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

        # TODO: Add error checking with alarms
        user = User.objects.create_user(username,email,password)

        context = {}

        return render(request, 'authentication/login.html', context)

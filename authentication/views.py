from authentication.models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    return HttpResponse("This is the authentication index")

@csrf_exempt
def login(request):

    if request.method == 'GET':
        return render(request,'authentication/login.html',context)
    elif request.method == 'POST':
        context = {}
        receivedData = json.loads(request.body.decode("utf-8"))
        username = receivedData["username"]
        password = receivedData["password"]
        user = authenticate(username=username, password=password)
        userData = User.objects.get(username=username)

        response = JsonResponse({
                'username': userData.username,
                'lastName': userData.first_name,
                'firstName': userData.last_name,
                'authenticaded': "true",
                'type': 'user_type',
            })

        return response

@csrf_exempt
def signUp(request):

    if request.method == 'GET':
        print("SIGN_UP GET")
        context = {}
        return render(request, 'authentication/signUp.html', context)
    elif request.method == 'POST':

        receivedData = json.loads(request.body.decode("utf-8"))

        username = receivedData["username"]
        password = receivedData["password"]
        firstName = receivedData["firstName"]
        lastName = receivedData["lastName"]
        email = receivedData["email"]
        user_type = receivedData["type"]

        print(receivedData)

        # TODO: Add error checking with alarms
        user = User.objects.create_user(username,email,password)
        userProfile = UserProfile(user=user, user_type=user_type) 
        user.first_name = firstName
        user.last_name = lastName
        user.save()

        response = JsonResponse({
                'lastLogin': user.last_login,
                'created': 'true',
            })

        return response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

@login_required
def index(request):
	context = {}
	return render(request, 'containers/index.html', context)



def create(request):
	return HttpResponse("This will be the create a containers view")

def run(request,container_id):
	return HttpResponse("This view will run the container #" + container_id)

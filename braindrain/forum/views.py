from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import NameForm

# Create your views here.

def index(request):
	return HttpResponse("it worked")

def thanks(request):
	return render(request, 'forum/thanks.html',)	

def login(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/thanks/')
	else:
		form = NameForm()
	return render(request, 'forum/name.html',{'form':form})	
	

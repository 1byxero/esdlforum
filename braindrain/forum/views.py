from django import forms
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import userForm,loginform
from .models import user
import hashlib



# Create your views here.

def index(request):
	return HttpResponse("it worked")

def thanks(request):
	return render(request, 'forum/thanks.html',)	

@csrf_exempt
def signup(request):
	if request.method == 'POST':
		form = userForm(request.POST)			
		if form.is_valid():				
				password = form.cleaned_data['password']
				if len(password)<10:
					alert = 'alert("Please enter password with more than 10 characters");'
					return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"signup"})				
				else:
					form.save()
					return HttpResponseRedirect('/thanks/')
			
	else:
		form = userForm()
	return render(request, 'forum/name.html',{'form':form,'title':"signup"})	


def login(request):
	if request.method == 'POST':
		#check if username and password is corret
		form = loginform(request.POST)

		if form.is_valid():						
			formusername = form.cleaned_data['username']
			formpassword = form.cleaned_data['password']
			try:
				userinstance = user.objects.get(username=formusername)
				if(userinstance.password==hashlib.md5(formpassword).hexdigest()):
					alert = 'alert("user verified");'
					return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"login"})
				else:
					alert = 'alert("Incorrect password");'
					return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"login"})
			except ObjectDoesNotExist:
				alert = 'alert("No user with given username exists");' #,%formusername
			 	return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"login"})				
	else:
		form = loginform()
		return render(request, 'forum/name.html',{'form':form,'title':"login"})	



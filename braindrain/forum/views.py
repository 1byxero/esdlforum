from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import userForm

# Create your views here.

def index(request):
	return HttpResponse("it worked")

def thanks(request):
	return render(request, 'forum/thanks.html',)	

def login(request):
	if request.method == 'POST':
		form = userForm(request.POST)		
		print dict(form.fields)
		# password = form.cleaned_data.get('password')
		# if(len(password)<10):
		# 	raise forms.ValidationError("Please enter password with more than 10 characters")
		# return password
		
		if form.is_valid():
			return HttpResponseRedirect('/thanks/')
	else:
		form = userForm()
	return render(request, 'forum/name.html',{'form':form})	
	

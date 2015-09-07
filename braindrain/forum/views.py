from django import forms
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import userForm,loginform,questionForm
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
	if "user" in request.session:			
			return redirect(profile)
	else:
		if request.method == 'POST':
			
			form = loginform(request.POST)

			if form.is_valid():						
				formusername = form.cleaned_data['username']
				formpassword = form.cleaned_data['password']
				try:
					userinstance = user.objects.get(username=formusername)
					if(userinstance.password==hashlib.md5(formpassword).hexdigest()):
						request.session['user'] = formusername
						return redirect(profile)
					else:
						alert = 'alert("Incorrect password");'
						return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"login"})
				except ObjectDoesNotExist:
					alert = 'alert("No user with given username exists");' #,%formusername
				 	return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"login"})
			else:
				form = loginform()
				alert = 'alert("Please enter password");' #,%formusername
				return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"login"})

		else:		
			form = loginform()
			return render(request, 'forum/name.html',{'form':form,'title':"login"})

@csrf_exempt
def profile(request):
	if "question" in request.POST:
		return redirect(askquestion)

	if "logout" in request.POST:		
		del request.session['user']
		return HttpResponse("successfully logged out")
	
	if 'user' in request.session:
		username = request.session['user']
		userinstance = user.objects.get(username=username)
		uid = userinstance.uid
		points = userinstance.points
		questionsasked = userinstance.questionsasked
		questionsanswered = userinstance.questionsanswered


		context = {
			'user':username,
			'uid':uid,
			'points':points,
			'questions':questionsasked,
			'answers':questionsanswered
		}
		return render(request, 'forum/profilepage.html',context)
	else:
		return HttpResponse("please login")

def askquestion(request):
	if 'user' in request.session:		
		if 'ask' in request.POST:
			form  = questionForm(request.POST)

			if form.is_valid():
				
				print form.cleaned_data
				return HttpResponse("form submitted")
			else:
				context = {
				'form':form,
				'user':request.session['user'],			
			}
			return render(request, 'forum/askquestion.html',context)


		else:
			form  = questionForm()
			
			context = {
				'form':form,
				'user':request.session['user'],
			}


			return render(request, 'forum/askquestion.html',context)

	else:
		return HttpResponse("please login")



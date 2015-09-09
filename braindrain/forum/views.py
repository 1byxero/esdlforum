from django import forms
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
import hashlib



# Create your views here.

loginalert = "please login<br>click <a href=/login>here</a> to login"

def index(request):
	if 'user' in request.session:	
		questionlist = question.objects.all()

		context = {
			'user':request.session['user'],
			'questionlist':questionlist,
		}

		return render(request, 'forum/index.html',context)
	else:
		questionlist = question.objects.all()

		context = {			
			'questionlist':questionlist,
		}

		return render(request, 'forum/index.html',context)


	# if 'user' in request.session:
	# 	#user personalized page
	# 	context {

	# 	}
	# 	return render(request,'forum/index.html',context)
	# else:
	# 	#generalized page
	# 	context {

	# 	}
	# 	return render(request,'forum/index.html',context)



@csrf_exempt
def signup(request):
	if "user" in request.session:
		return redirect(profile)
	else:
		if request.method == 'POST':
			form = userForm(request.POST)			
			if form.is_valid():				
					password = form.cleaned_data['password']
					if len(password)<10:					
						alert = 'alert("Please enter password with more than 10 characters");'
						return render(request, 'forum/name.html',{'form':form,'alert':alert,'title':"signup"})				
					else:
						a = form.save(commit=False)
						a.password = hashlib.md5(a.password).hexdigest()
						a.save()
						return HttpResponse('You have been success fully registered<br>click <a href=/login>here</a> to login')
				
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
		return HttpResponse(loginalert)

def askquestion(request):
	if 'user' in request.session:
		loggeduser = request.session['user']		
		if 'ask' in request.POST:			
			form  = questionForm(request.POST)

			if form.is_valid():

				editableform = form.save(commit=False)
				editableform.askedby = user.objects.get(username=loggeduser)
				editableform.save()
				userinstancetoupdatequestionasked = user.objects.get(username=loggeduser)
				userinstancetoupdatequestionasked.questionsasked = userinstancetoupdatequestionasked.questionsasked + 1
				userinstancetoupdatequestionasked.save()
				return HttpResponse("form submitted")
			else:
				context = {
				'form':form,
				'user':loggeduser,			
			}
			return render(request, 'forum/askquestion.html',context)


		else:
			form  = questionForm()
			
			context = {
				'form':form,
				'user':loggeduser,
			}


			return render(request, 'forum/askquestion.html',context)

	else:
		return HttpResponse(loginalert)

def answerquestion(request):
	if 'user' in request.session:
		try:
			qid = request.GET.get('qid')
			questioninst = question.objects.get(qid=qid)
			questiontitle = questioninst.questiontitle
			questioncontent = questioninst.questioncontent

			userlogged = request.session['user']		
			if request.method == 'POST':
				form = answerquestionForm(request.POST)

				if form.is_valid():
					print form.cleaned_data
					answer = form.cleaned_data['answer']
					if(len(answer)<200):
						print len(answer)
						alert = 'alert("Your answer is too short to submit");'
						suggestion = "Elaborate your answer. Share all you've got!"
						context = {
							'form':form,
							'alert':alert,
							'suggestion':suggestion,
							'user':userlogged,
							'questiontitle':questiontitle,
							'questioncontent':questioncontent,						
						}
						return render(request,'forum/answerquestion.html',context)
					else:
						alert = 'alert("Your answer will be submited");'					
						context = {
							'form':form,
							'alert':alert,						
							'user':userlogged,
							'questiontitle':questiontitle,
							'questioncontent':questioncontent,						
						}
						return render(request,'forum/answerquestion.html',context)

			if request.method == 'GET':			
				form = answerquestionForm()		

				context = {
							'form':form,						
							'user':userlogged,
							'questiontitle':questiontitle,
							'questioncontent':questioncontent,
						}
				return render(request,'forum/answerquestion.html',context)
		except ObjectDoesNotExist:			
			return HttpResponse("No such question exists<br>")

	else:
		return HttpResponse(loginalert)


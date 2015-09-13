from django import forms
from django.core.mail import send_mail
from django.conf import settings
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
				sendmailid = userinstancetoupdatequestionasked.email
				mailsubject = "Notifications for Question"
				mailbody = "Hello "+userinstancetoupdatequestionasked.name+"!\nWe will notify you when the question you've asked receives an answer!"
				
				send_mail(
					mailsubject,
					mailbody,
					settings.EMAIL_HOST_USER,
					[sendmailid],
					fail_silently=False)


				return HttpResponse("Question submitted")
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
		loggeduser = request.session['user']	

		if request.method == 'POST':
			#executed if answer form is written and posted

			if 'qid' in request.POST:				
				qid = request.POST.get('qid')				
				try:
					form = answerquestionForm(request.POST)								
					questioninst = question.objects.get(qid=qid)
					#execute this block is qid exists
					questiontitle = questioninst.questiontitle
					questioncontent = questioninst.questioncontent					
					askedby = questioninst.askedby
					answered = questioninst.answered
					answerlist = []
					answercontent = ""

					if answered:
						answerinst = answer.objects.filter(question=qid)
						for i in answerinst:
							answercontentinmodel = i.answercontent
							answeredbyinmodel = i.useranswered
							answerlistobject = 	{'answer':answercontentinmodel,'by':answeredbyinmodel,}
					 		answerlist.append(answerlistobject)
		
					if form.is_valid():
						#execute this if form is valid							
						answercontent = form.cleaned_data['answer']
						if(len(answercontent)<100):						
							alert = 'alert("Your answer is too short to submit");'
							suggestion = "Elaborate your answer. Share all you've got!"												
							context = {
								'qid':qid,
								'form':form,
								'user':loggeduser,
								'alert':alert,															
								'askedby':askedby,
								'suggestion':suggestion,
								'questiontitle':questiontitle,
								'questioncontent':questioncontent,						
								'answered':answered,
								'answercontent':answercontent,
								'answerlist':answerlist,
							}
							return render(request,'forum/answerquestion.html',context)
						else:
							userinst = user.objects.get(username=loggeduser)

							answermodel = answer(answercontent=answercontent,useranswered=userinst,question=questioninst)
							answermodel.save()
							#saved answer
							questioninst.answered = True
							questioninst.save()
							#updated question field								
							userinst.questionsanswered = userinst.questionsanswered+1
							userinst.save()

							userwhoaskedquestioninst=user.objects.get(username=askedby)
							sendmailid = userwhoaskedquestioninst.email
							sendmailsubject = "Your question was answered!"
							sendmailbody = "Hello "+userwhoaskedquestioninst.name+"!\nYour question with title "+questioninst.questiontitle+" has received an answer!"

							send_mail(
								sendmailsubject,
								sendmailbody,
								settings.EMAIL_HOST_USER,
								[sendmailid],
								fail_silently=False)

							return HttpResponse("Your answer will be submited")
						
					else:
						#execute this block if form is not valid 
						context = {
							'qid':qid,
							'form':form,
							'user':loggeduser,
							'askedby':askedby,
							'questiontitle':questiontitle,
							'questioncontent':questioncontent,
							'answered':answered,
							'answercontent':answercontent,
							'answerlist':answerlist,				
						}
						return render(request,'forum/answerquestion.html',context)					
				except ObjectDoesNotExist:
					#post request forging handled by this block					
					print "first"
					return HttpResponse("Something went Wrong!<br>Click <a href='/'>here</a> to check the questions")					

			else:
				#post request forging handled by this block				
				print "second"
				return HttpResponse("Something went Wrong!<br>Click <a href='/'>here</a> to check the questions")	

		elif 'qid' in request.GET:
			#this block is executed if 

			qid = request.GET.get('qid')
			questioninst = question.objects.filter(qid=qid)
			if questioninst:
				questioninst = question.objects.get(qid=qid)
				questiontitle = questioninst.questiontitle
				questioncontent = questioninst.questioncontent
				askedby = questioninst.askedby				
				answered = questioninst.answered
				answerlist = []
				answercontent = ""

				if answered:					
					answerinst = answer.objects.filter(question=qid)
					for i in answerinst:						
						answercontentinmodel = i.answercontent
						answeredbyinmodel = i.useranswered
						answerlistobject = 	{'answer':answercontentinmodel,'by':answeredbyinmodel,}
				 		answerlist.append(answerlistobject)

				form = answerquestionForm()		

				context = {
							'qid':qid,
							'form':form,						
							'user':loggeduser,
							'askedby':askedby,
							'questiontitle':questiontitle,
							'questioncontent':questioncontent,
							'answered':answered,
							'answercontent':answercontent,
							'answerlist':answerlist,
						}
				return render(request,'forum/answerquestion.html',context)
			else:
				return HttpResponse("no such question exists!<br>Click <a href='/'>here</a> to check the questions")
		else:
			return HttpResponse("Select the question first!<br>Click <a href='/'>here</a> to check the questions")	
	else:
		return HttpResponse(loginalert)





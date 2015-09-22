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
	questionlist = question.objects.all()
	showquestions=True

	if len(questionlist)==0:
		showquestions=False

	if 'user' in request.session:		

		context = {
			'showquestions':showquestions,
			'user':request.session['user'],
			'questionlist':questionlist,
		}

		return render(request, 'forum/index.html',context)
	else:
		context = {
			'showquestions':showquestions,		
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
						return render(request, 'forum/signuplogin.html',{'form':form,'alert':alert,'title':"signup"})				
					else:
						a = form.save(commit=False)
						a.password = hashlib.md5(a.password).hexdigest()
						a.save()
						return HttpResponse('You have been success fully registered<br>click <a href=/login>here</a> to login')
				
		else:
			form = userForm()
		return render(request, 'forum/signuplogin.html',{'form':form,'title':"signup"})	


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
						return render(request, 'forum/signuplogin.html',{'form':form,'alert':alert,'title':"login"})
				except ObjectDoesNotExist:
					alert = 'alert("No user with given username exists");' #,%formusername
				 	return render(request, 'forum/signuplogin.html',{'form':form,'alert':alert,'title':"login"})
			else:
				form = loginform()
				alert = 'alert("Please enter password");' #,%formusername
				return render(request, 'forum/signuplogin.html',{'form':form,'alert':alert,'title':"login"})

		else:		
			form = loginform()
			return render(request, 'forum/signuplogin.html',{'form':form,'title':"login"})

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
		isteacher = userinstance.isteacher

		questionaskedlist = question.objects.filter(askedby=userinstance)		

		context = {
			'user':username,
			'uid':uid,			
			'questionlist':questionaskedlist,			
		}

		if isteacher:
			questionaskedtoyoulist = question.objects.filter(askedto=userinstance)
			noofquestionsasked = questionaskedtoyoulist.count()				
			if noofquestionsasked>0:
				showquestionsaskedtoyou = True
			else:
				showquestionsaskedtoyou = False
			context.update({"questionaskedtoyoulist":questionaskedtoyoulist,'showquestionsaskedtoyou':showquestionsaskedtoyou,})		
		return render(request, 'forum/profilepage.html',context)
	else:
		return HttpResponse(loginalert)

def checkquestionexists(request):
	if 'user' in request.session:
		if request.method == 'POST':
			form = searchquestionForm(request.POST)

			if form.is_valid():
				stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
				searchquestion = str(form.cleaned_data['question']).split(" ")

				questiontags=[]
				for i in searchquestion:
					if i.lower() not in stopwords:
						questiontags.append(i)

			else:
				print "not valid"				

			context = {
				'form':form
			}

			return render(request,'forum/search.html',context)			
		else:
			form = searchquestionForm()
			context = {
				'form':form
			}
			return render(request,'forum/search.html',context) 			
		
		
	else:
		return HttpResponse(loginalert)

@csrf_exempt
def askquestion(request):
	if 'user' in request.session:
		loggeduser = request.session['user']		
		if 'ask' in request.POST:			
			form  = questionForm(request.POST)

			if form.is_valid():								
				if form.cleaned_data['isonetoone'] and form.cleaned_data['askedto']==None:
					alert = "alert('Select teacher to whom you want to ask the question!');"
					context = {
						'form':form,
						'user':loggeduser,
						'alert':alert,
						}
					return render(request, 'forum/askquestion.html',context)
				else:																			
					questiontitle = form.cleaned_data['questiontitle']
					questioncontent = form.cleaned_data['questioncontent']
					isonetoone = form.cleaned_data['isonetoone']																					
					askedby = user.objects.get(username=loggeduser)
					if isonetoone:
						askedto = form.cleaned_data['askedto']
						questioninst = question(questiontitle=questiontitle,questioncontent=questioncontent,isonetoone=isonetoone,askedto=askedto,askedby=askedby)
						sendmailidtoteacher = askedto.email
						mailsubjecttoteacher = "A question was asked to you!"
						mailbodytoteacher = "Hello "+askedto.name+"!\nA question was asked to you by "+askedby.name+"!"
						send_mail(
							mailsubjecttoteacher,
							mailbodytoteacher,
							settings.EMAIL_HOST_USER,
							[sendmailidtoteacher],
							fail_silently=False)
					else:
						questioninst = question(questiontitle=questiontitle,questioncontent=questioncontent,isonetoone=isonetoone,askedby=askedby)
					questioninst.save()										
					#here askedby has model instance of question asker
					sendmailid = askedby.email
					mailsubject = "Notifications for Question"
					mailbody = "Hello "+askedby.name+"!\nWe will notify you when the question you've asked receives an answer!"					
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
					askedto = questioninst.askedto
					cananswer = True
					if askedto!=None and askedto!=user.objects.get(username=loggeduser):
						cananswer = False

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
								'cananswer':cananswer,
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
							'cananswer':cananswer,
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
					return HttpResponse("Something went Wrong!<br>Click <a href='/'>here</a> to check the questions")					

			else:
				#post request forging handled by this block								
				return HttpResponse("Something went Wrong!<br>Click <a href='/'>here</a> to check the questions")	

		elif 'qid' in request.GET:
			#this block is executed if when the question link on index page is executed

			qid = request.GET.get('qid')
			questioninst = question.objects.filter(qid=qid)
			if questioninst:
				questioninst = question.objects.get(qid=qid)
				questiontitle = questioninst.questiontitle
				questioncontent = questioninst.questioncontent
				askedby = questioninst.askedby				
				answered = questioninst.answered
				askedto = questioninst.askedto	


				answerlist = []
				answercontent = ""
				cananswer = True

				if answered:					
					answerinst = answer.objects.filter(question=qid)
					for i in answerinst:						
						answercontentinmodel = i.answercontent
						answeredbyinmodel = i.useranswered
						answerlistobject = 	{'answer':answercontentinmodel,'by':answeredbyinmodel,}
				 		answerlist.append(answerlistobject)

				form = answerquestionForm()						
				if askedto!=None and askedto!=user.objects.get(username=loggeduser):
					cananswer = False


				context = {							
							'qid':qid,
							'form':form,
							'cananswer':cananswer,
							'askedby':askedby,							
							'user':loggeduser,							
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





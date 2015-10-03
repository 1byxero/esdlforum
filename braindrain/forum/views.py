from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .forms import *
from .models import *
import hashlib



# Create your views here.

loginalert = "please login<br>click <a href=/login>here</a> to login"

def index(request):
	if 'tags' in request.POST:
		tag = request.POST.get('tags')
		questionlist = question.objects.filter(tag=tag)
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

	else:
			form = selecttagForm()
			context = {
				'user':request.session['user'],
				'showtagform':True,
				'showquestions':False,
				'form':form,				
			}

			return render(request, 'forum/index.html',context)






@csrf_exempt
def signup(request):
	if "user" in request.session:
		return redirect(profile)

	else:
		if request.method == 'POST':
			form = tempuserForm(request.POST)

			if form.is_valid():
				email = form.cleaned_data['email']

				hashingtext = email+str(datetime.now()) #got hashtext
				hashingtext = hashlib.md5(hashingtext).hexdigest()

				tempuserinst = tempusers(email=email,hashlink=hashingtext)
				tempuserinst.save()

				#print request.current_path
				currentlink = request.build_absolute_uri()

				mailsubject = "Signup Process"
				linkforsignup=currentlink+"?hash="+hashingtext
				mailbody = "Hello!\nPlease click on following link to proceed further for signup!\n"+linkforsignup
				sendmailid = email

				send_mail(
					mailsubject,
					mailbody,
					settings.EMAIL_HOST_USER,
					[sendmailid],
					fail_silently=False)

				context = {
						"suggestion":"Please check your mail for further process!",
						}					
				return render(request,"forum/response.html",context)

				

			else:
				alert = "Oops Something Went wrong"
				context = {
				'alert':alert,
				'form':form,
				'title':"signup",
			}
			return render(request, 'forum/signuplogin.html',context)



		elif 'hash' in request.GET:
			hashtext = request.GET.get('hash')

			try:
				checkrequest = tempusers.objects.get(hashlink=hashtext)
				if checkrequest.hashlink == hashtext:					
					context = {
						"suggestion":"Click <a href=/signupinfo?hash="+hashtext+">here</a> to signup!",
					}
					return render(request,"forum/response.html",context)

				else:
					context = {
						"suggestion":"Something went Wrong!",
					}					
					return render(request,"forum/response.html",context)

			except ObjectDoesNotExist:
				context = {
						"suggestion":"Trying to be smart?",
					}					
				return render(request,"forum/response.html",context)
				


			#add normal signup here

		else:
			form = tempuserForm()
			suggestion = "Enter email id, we will send you signup link!"

			context = {
				'suggestion':suggestion,
				'form':form,
				'title':"signup",
			}
			return render(request, 'forum/signuplogin.html',context)

def signupinfo(request):
	if 'user' in request.session:
		return redirect(profile)
	else:
		if request.method == "POST":
			if 'hash' in request.POST:
				form = userForm(request.POST)

				if form.is_valid():
					email = form.cleaned_data['email']
					password = form.cleaned_data['password']
					if len(password)<10:
						alert = 'alert("Please enter password with more than 10 characters");'
						return render(request, 'forum/signuplogin.html',{'form':form,'alert':alert,'title':"signup"})
					else:
						a = form.save(commit=False)
						if "@pict.edu" in email:
							a.isteacher = True
						a.password = hashlib.md5(a.password).hexdigest()
						a.save()
						tempusers.objects.filter(email=email).delete()
						context = {
						"suggestion":'You have been success fully registered<br>click <a href=/login>here</a> to login',
						}					
						return render(request,"forum/response.html",context)
						

				else:
					form = userForm(request.POST)
					context = {
					'form':form,
					'title':"signup",
					}
					return render(request, 'forum/realsignup.html',context)


			else:
				context = {
						"suggestion":"Trying to be smart?<br>are yeh?",
						}					
				return render(request,"forum/response.html",context)
				


		else:
			hashtext = request.GET.get('hash')
			try:
				checkrequest = tempusers.objects.get(hashlink=hashtext)
				if checkrequest.hashlink == hashtext:
					form = userForm()
					form.fields['email'].initial=checkrequest.email
					context = {
					'hash':hashtext,
					'form':form,
					'title':"signup",
					}
					return render(request, 'forum/realsignup.html',context)
				else:
					context = {
						"suggestion":"Trying to be smart?<br>are yeh?",
						}					
					return render(request,"forum/response.html",context)
					

			except ObjectDoesNotExist:
				context = {
						"suggestion":"Trying to be smart?<br>are yeh?",
						}					
				return render(request,"forum/response.html",context)





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
						return redirect(index)
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
	if "show" in request.POST:
		return redirect(index)

	if "question" in request.POST:
		return redirect(search)

	if "logout" in request.POST:
		del request.session['user']
		context = {
						"suggestion":"successfully logged out",
						}					
		return render(request,"forum/response.html",context)	

	if 'user' in request.session:
		username = request.session['user']
		userinstance = user.objects.get(username=username)
		uid = userinstance.uid
		isteacher = userinstance.isteacher

		questionaskedlist = question.objects.filter(askedby=userinstance)
		questionsyouasked = False
		if questionaskedlist.count()>0:
			questionsyouasked = True

		context = {
			'questionsyouasked':questionsyouasked,
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
@csrf_exempt
def search(request):
	if 'user' in request.session:
		user = request.session['user']
		if request.method == 'POST':
			showquestions = False
			form = searchquestionForm(request.POST)

			if form.is_valid():

				stopwords = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes', 'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down', 'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible', 'present', 'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z', 'afterwards', 'am', 'amongst', 'amoungst', 'amount', 'anyhow', 'anyway', 'becoming', 'beforehand', 'below', 'beside', 'besides', 'beyond', 'bill', 'bottom', 'call', 'cant', 'co', 'con', 'couldnt', 'cry', 'de', 'describe', 'detail', 'due', 'eg', 'eight', 'eleven', 'else', 'elsewhere', 'empty', 'etc', 'except', 'fifteen', 'fify', 'fill', 'fire', 'five', 'former', 'formerly', 'forty', 'found', 'front', 'hasnt', 'hence', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'hundred', 'ie', 'inc', 'indeed', 'latter', 'latterly', 'ltd', 'meanwhile', 'mill', 'mine', 'moreover', 'move', 'name', 'namely', 'neither', 'nevertheless', 'nine', 'none', 'nor', 'onto', 'otherwise', 'ours', 'ourselves', 'own', 'please', 're', 'serious', 'sincere', 'six', 'sixty', 'somehow', 'sometime', 'sometimes', 'system', 'ten', 'themselves', 'thence', 'thereafter', 'thereby', 'therein', 'thereupon', 'thickv', 'thin', 'third', 'throughout', 'thru', 'top', 'towards', 'twelve', 'twenty', 'un', 'via', 'whatever', 'whence', 'whenever', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whither', 'whoever', 'whom', 'yourself', 'yourselves']

				searchquestion = str(form.cleaned_data['question']).split(" ")

				questiontags=[]

				for i in searchquestion:
					if i.lower() not in stopwords:
						questiontags.append(i)

				questiontagswithoutspecialchars = []

				for i in questiontags:
					check = ''.join(e for e in i if e.isalnum())
					questiontagswithoutspecialchars.append(check.lower())


				searchresult = []
				finalresults = []

				for i in questiontagswithoutspecialchars:
					results = question.objects.filter(tag=i)
					titleresult = question.objects.filter(questiontitle=i)
					if results.count()>0 or titleresult.count()>0:
						showquestions = True
						for i in results:
							searchresult.append(i)
						for i in titleresult:
							if i not in searchresult:
								searchresult.append(i)


				

				if showquestions:
					for i in searchresult:
						finalresults.append(i)

					

				context = {
						'user':user,
					}

				if len(searchresult)>0:
					context = {
						'user':user,
						'showquestions':showquestions,
						'questionlist':finalresults,
					}

				return render(request,"forum/searchresult.html",context)



			else:

				context = {
					'user':request.session['user'],
					'form':form,
					'alert':"Something Went Wrong!",
				}

				return render(request,"forum/signuplogin.html",context)

		else:
			form = searchquestionForm()

			context = {
				'user':request.session['user'],
				'form':form,
			}

			return render(request,'forum/searchpage.html',context)

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
					tags = form.cleaned_data['tags']
					questioncontent = form.cleaned_data['questioncontent']
					isonetoone = form.cleaned_data['isonetoone']
					askedby = user.objects.get(username=loggeduser)
					if isonetoone:
						askedto = form.cleaned_data['askedto']
						questioninst = question(questiontitle=questiontitle,questioncontent=questioncontent,isonetoone=isonetoone,askedto=askedto,askedby=askedby,tag=tags)
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
						questioninst = question(questiontitle=questiontitle,questioncontent=questioncontent,isonetoone=isonetoone,askedby=askedby,tag=tags)
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

					context = {
						"suggestion":"Question submitted",
					}
					return render(request,"forum/response.html",context)

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
							context = {
										"suggestion":"Your answer will be submited",
									}					
							return render(request,"forum/response.html",context)							

					else:		


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

					context = {
						"suggestion":"Something went Wrong!<br>Click <a href='/'>here</a> to check the questions",
						}					
					return render(request,"forum/response.html",context)
					

			else:
				#post request forging handled by this block
				context = {
						"suggestion":"Something went Wrong!<br>Click <a href='/'>here</a> to check the questions",
						}					
				return render(request,"forum/response.html",context)

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
				context = {
						"suggestion":"no such question exists!<br>Click <a href='/'>here</a> to check the questions",
						}					
				return render(request,"forum/response.html",context)
				
		else:
			context = {
						"suggestion":"no such question exists!<br>Click <a href='/'>here</a> to check the questions",
						}					
			return render(request,"forum/response.html",context)
	else:
		return HttpResponse(loginalert)



def addtag(request):
	if 'user' in request.session:
		if request.method =="POST":			
			form = addtagForm(request.POST)	

			if form.is_valid():
				form.save()
				context = {
						"user":request.session['user'],
						"suggestion":"Tag added",
						}					
				return render(request,"forum/response.html",context)				

			else:
				context = {				
				"user":request.session['user'],
				"suggestion":"tag added",				
				'form':form,
				}

			return render(request,"forum/addtag.html",context)

		else:
			showtags=tags.objects.all()

			form = addtagForm()
			context = {
				"user":request.session['user'],
				"availabletags":showtags,
				"form":form,
			}

			return render(request,"forum/addtag.html",context)	

	else:
		context = {
						"suggestion":loginalert,
						}					
		return render(request,"forum/response.html",context)
		return HttpResponse(loginalert)
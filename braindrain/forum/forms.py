from django import forms
from .models import *
import hashlib

class userForm(forms.ModelForm):
	class Meta:
		model = user
		exclude = ['uid','questionsasked','questionsanswered','points']
		widgets = {
		'password': forms.PasswordInput(),
		}

class loginform(forms.Form):	
	username = forms.CharField(label='Username', max_length=100,required = True)
	password = forms.CharField(label='Password', max_length=100,required = True,widget = forms.PasswordInput())

class questionForm(forms.Form):
	questiontitle = forms.CharField(label='Question Title', max_length=100,required = True)
	questioncontent = forms.CharField(label='Question',required = True,widget=forms.Textarea)
	isonetoone = forms.BooleanField(label= 'Ask to teacher',required=False)	
	askedto = forms.ModelChoiceField(label='Question asked to',queryset=user.objects.filter(isteacher=True),required=False)





class answerquestionForm(forms.Form):	
	answer = forms.CharField(label='answer',required=True,widget=forms.Textarea)


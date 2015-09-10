from django import forms
from .models import user,question
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

class questionForm(forms.ModelForm):
	class Meta:
		model = question
		fields = ['questiontitle','questioncontent']

class aanswerquestionForm(forms.Form):
	qid = forms.IntegerField(editable=False)
	answer = forms.CharField(label='answer',required=True,widget=forms.Textarea)

class answerquestionForm(forms.ModelForm):
	class Meta:
		model = answer

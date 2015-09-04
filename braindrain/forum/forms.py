from django import forms
from .models import user

class userForm(forms.ModelForm):
	class Meta:
		model = user
		#fields = ['name','email','username','password']
		exclude = ['uid']
		widgets = {
		'password': forms.PasswordInput(),
		}

	def doyourvalidation(self):
		print forms.ModelForm.cleaned_data.get('password')
		#print password+"asss"
		passlen = len(str(password))

		if(passlen<10):
			print passlen
			raise forms.ValidationError("Please enter password with more than 10 characters")
		return password


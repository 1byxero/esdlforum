from django.db import models


class user(models.Model):
	uid = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)	
	username = models.CharField(max_length=200,unique = True)
	password = models.CharField(max_length=200)
	points = models.IntegerField(default = 0)
	questionsasked = models.IntegerField(default = 0)
	questionsanswered = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.username

#class question(models.Model):
	# def __unicode__(self):
	# 	return self


class answer(models.Model):
	aid = models.IntegerField(primary_key=True)
	answercontent = models.CharField(max_length=2000,blank = False)
	user = models.ForeignKey('user')	
	#question = models.ForeignKey('question')

	def __unicode__(self):
		return self.aid


	

	




# Create your models here.

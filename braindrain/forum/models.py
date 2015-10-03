from django.db import models


class tempusers(models.Model):
	email = models.EmailField(max_length=200)
	hashlink = models.CharField(max_length=200)

	def __unicode__(self):
		return self.email

class user(models.Model):
	uid = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)	
	username = models.CharField(max_length=200,unique = True)
	password = models.CharField(max_length=200)	
	isteacher = models.BooleanField(default=False)

	def __unicode__(self):
		return self.username

class question(models.Model):
	#these are normal questions
	qid = models.IntegerField(primary_key=True)
	questiontitle = models.CharField(max_length=200,blank = False)
	questioncontent = models.TextField(blank = False)
	answered = models.BooleanField(default = False)
	askedby = models.ForeignKey('user', related_name='askedby')
	askedto = models.ForeignKey('user', related_name='askedto',null=True,blank=True)
	isonetoone = models.BooleanField(default=False)
	tag = models.ForeignKey('tags',null=True,blank=True)	
	#tags	
	#importance	

	def __unicode__(self):
		return self.questiontitle


class answer(models.Model):
	aid = models.IntegerField(primary_key=True)
	answercontent = models.TextField(blank = False)
	useranswered = models.ForeignKey('user')	
	question = models.ForeignKey('question',null = True)

	def __unicode__(self):
		questioninst = question.objects.filter(questiontitle=self.question)
		return str(self.aid)

	
class tags(models.Model):	
	name = models.CharField(max_length=30,blank=False,primary_key=True)

	def __unicode__(self):
		return self.name

	




# Create your models here.

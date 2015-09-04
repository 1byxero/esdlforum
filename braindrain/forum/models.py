from django.db import models


class user(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	#regid = models.CharField(max_length=200)
	username = models.CharField(max_length=200,)
	password = models.CharField(max_length=200)
	uid = models.IntegerField(primary_key=True)

	class Meta:
		app_label = 'forum_user'

	def __unicode__(self):
		return self.email




# Create your models here.

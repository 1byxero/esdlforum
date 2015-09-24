from django.contrib import admin
from .models import *

class userAdmin(admin.ModelAdmin):
	pass

class questionAdmin(admin.ModelAdmin):
	pass

class answerAdmin(admin.ModelAdmin):
	pass

class tagsAdmin(admin.ModelAdmin):
	pass


admin.site.register(user,userAdmin)
admin.site.register(question,questionAdmin)
admin.site.register(answer,answerAdmin)
admin.site.register(tags,tagsAdmin)



# Register your models here.

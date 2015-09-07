from django.contrib import admin
from .models import user,question,answer

class userAdmin(admin.ModelAdmin):
	pass

class questionAdmin(admin.ModelAdmin):
	pass

class answerAdmin(admin.ModelAdmin):
	pass

admin.site.register(user,userAdmin)
admin.site.register(question,questionAdmin)
admin.site.register(answer,answerAdmin)



# Register your models here.

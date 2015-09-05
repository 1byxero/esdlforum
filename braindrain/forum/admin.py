from django.contrib import admin
from .models import user

class userAdmin(admin.ModelAdmin):
	pass

admin.site.register(user,userAdmin)



# Register your models here.

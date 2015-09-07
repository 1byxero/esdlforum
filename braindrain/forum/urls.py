from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),        
    url(r'^login/', views.login, name='login'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^askquestion/', views.askquestion, name='askquestion'),

]


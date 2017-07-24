# exqna/urls.py
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.exquestion, name='exquestion'),
=======
    url(r'^(?P<user_id>\d+)/$', views.exquestion, name='exquestion'),
    url(r'^(?P<user_id>\d+)/required/$', views.required, name='required'),
    # url(r'^(?P<user_id>\d+)/already_required/$', views.already_required, name='already_required'),
    url(r'^(?P<answer_id>\d+)/edit/$', views.exq_edit, name='exq_edit'),
>>>>>>> fe062aba711e97ab9684214deeaf660b700fb40e
]
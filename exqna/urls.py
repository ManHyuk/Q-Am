# exqna/urls.py
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.exquestion, name='exquestion'),
    url(r'^(?P<user_id>\d+)/$', views.exquestion, name='exquestion'),
    url(r'^(?P<user_id>\d+)/required/$', views.required, name='required'),
    url(r'^(?P<ex_answer_id>\d+)/edit/$', views.exquestion_edit, name='exquestion_edit'),
    url(r'^(?P<ex_answer_id>\d+)/detail/$',views.exquestion_detail, name='exquestion_detail')
    # url(r'^(?P<user_id>\d+)/already_required/$', views.already_required, name='already_required'),
]

# qna/urls.py
from django.conf.urls import url, include
from django.contrib import admin
from qna import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.question, name='question'),
    url(r'^main/$', views.main, name='main'),
    url(r'^(?P<answer_id>\d+)/edit/$', views.question_edit, name='question_edit'),
    # url(r'^(?P<user_id>\d+)/answer_list/$', views.answer_list, name='answer_list'),
]

from django.conf.urls import url, include
from django.contrib import admin
from qna import views

urlpatterns = [
    url(r'^$', views.question, name='question'),
    url(r'^(?P<id>\d+)/submit/$', views.question_submit,name='question_submit'),
    url(r'^(?P<id>\d+)/edit/$', views.question_edit,name='question_edit'),
]

from django.conf.urls import url, include
from django.contrib import admin
from qna import views

urlpatterns = [
    url(r'^$', views.question, name='question'),
    url(r'^answer_submit/(?P<id>\d+)', views.answer_submit,name='answer_submit'),
    url(r'^main/$', views.main, name='main'),
]

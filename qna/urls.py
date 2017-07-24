from django.conf.urls import url, include
from django.contrib import admin
from qna import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)$',views.question,name='question'),
    url(r'^main/$',views.main,name='main'),
    url(r'^search/$',views.question_search,name='question_search'),
    url(r'^(?P<answer_id>\d+)/detail/$',views.question_detail,name='question_detail'),
    url(r'^(?P<answer_id>\d+)/edit/$', views.question_edit,name='question_edit'),
]

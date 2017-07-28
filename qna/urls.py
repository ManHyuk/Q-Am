from django.conf.urls import url, include
from django.contrib import admin
from qna import views



urlpatterns = [
    url(r'^$',views.question,name='question'),
    url(r'^main/$',views.main,name='main'),
    url(r'^search/$',views.question_search,name='question_search'),
    url(r'^search_day$',views.question_search_day, name='question_search_day'),
    url(r'^search_content$',views.question_search_content,name='question_search_content'),
    url(r'^other/$', views.other_people, name='other_people'),
    url(r'^(?P<question_id>\d+)/detail/$',views.question_detail,name='question_detail'),
    url(r'^(?P<answer_id>\d+)/edit/$',views.question_edit,name='question_edit'),
]

from django.conf.urls import url, include
from django.contrib import admin
from qna import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.index, name='index'),
    url(r'^main/$', views.index, name='main'),
=======
    url(r'^$', views.question, name='question'),
    url(r'^answer_submit/(?P<id>\d+)', views.answer_submit,name='answer_submit'),
>>>>>>> 7940e4eee71cc93c4fa2d9d0e9f37be5a5345278
]

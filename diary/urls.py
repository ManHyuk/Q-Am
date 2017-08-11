from django.conf.urls import url, include
from django.contrib import admin
from diary import views

urlpatterns = [
    url(r'^$', views.diary_list, name='diary_list'),
    url(r'^search_title/$',views.diary_search_title, name='diary_search_title'),
    url(r'^search_content/$',views.diary_search_content, name='diary_search_content'),
    url(r'^search_day/$',views.diary_search_day, name='diary_search_day'),
    url(r'^new/$', views.diary_new, name='diary_new'),
    url(r'^(?P<pk>\d+)/detail/$', views.diary_detail, name='diary_detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.diary_edit, name='diary_edit'),
    url(r'^(?P<pk>\d+)/del/$', views.diary_delete, name='diary_delete'),
]

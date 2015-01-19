# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
    url(r'^$', MyProfileView.as_view(), name='my_profile'),
    url(r'^pdfdocuments/$', MyPDFDocumentsView.as_view(), name='my_pdfdocuments'),
    url(r'^(?P<username>[\w.@+-]+)/$', user_redirect_view, name='user_detail'),
    url(r'^(?P<username>[\w.@+-]+)/info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^(?P<username>[\w.@+-]+)/pdfdocuments/$', UserPDFDocumentsView.as_view(), name='user_pdfdocuments'),
    url(r'^(?P<username>[\w.@+-]+)/projects/$', UserProjectsView.as_view(), name='user_projects'),
    url(r'^(?P<username>[\w.@+-]+)/project/new/$', ProjectCreateView.as_view(), name='project_create'),
    url(r'^(?P<username>[\w.@+-]+)/project/(?P<pk>\d+)/edit/$', ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<username>[\w.@+-]+)/project/(?P<pk>\d+)/delete/$', ProjectDeleteView.as_view(), name='project_delete'),
)

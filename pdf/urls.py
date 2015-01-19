# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url,include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from .views import doc_detail,doc_list,doc_upload
from django.conf.urls.static import static
from django.conf import settings
from pdf.models import Category, PDFDocument
#from accounts.models import User

from django.views.generic import RedirectView
from .views import *
from .feeds import RecentPDFDocumentsRss, CategoryRecentPDFDocumentsRss, RecentPDFDocumentsAtom, CategoryRecentPDFDocumentsAtom
#from accounts.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', pdfdocument_home, name='pdfdocument_home'),
    #url(r'^rss/$', RecentPDFDocumentsRss(), name='pdfdocument_feed_rss'),
    #url(r'^atom/$', RecentPDFDocumentsAtom(), name='pdfdocument_feed_atom'),
    url(r'^category/new/$', permission_required('pdfdocuments.add_category', raise_exception=True)(CategoryCreateView.as_view()), name='category_create'),
    url(r'^category/(?P<slug>[-\w]+)/$', category_home, name='pdfdocument_category_home'),
    url(r'^category/(?P<slug>[-\w]+)/edit/$', CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<category_slug>[-\w]+)/rss/$', CategoryRecentPDFDocumentsRss(), name='category_feed_rss'),
    url(r'^category/(?P<category_slug>[-\w]+)/atom/$', CategoryRecentPDFDocumentsAtom(), name='category_feed_atom'),
    url(r'^category/(?P<slug>[-\w]+)/follow/$', CategoryFollowView.as_view(), name='category_follow'),
    url(r'^category/(?P<slug>[-\w]+)/all/$', PDFDocumentCategoryListView.as_view(), name='pdfdocument_category_list_all'),
    url(r'^category/(?P<slug>[-\w]+)/offline/$', RedirectView.as_view(url='/pdfdocuments/', permanent=True)), #Removed offline resource_type
    url(r'^category/(?P<slug>[-\w]+)/documentation/$', RedirectView.as_view(url='/pdfdocuments/', permanent=True)), #Removed documentation resource_type
    url(r'^category/(?P<slug>[-\w]+)/(?P<pdfdocument_type>[-\w]+)/$', PDFDocumentCategoryListView.as_view(), name='pdfdocument_category_list'),
    url(r'^(?P<pk>\d+)/$', PDFDocumentDetailView.as_view(), name='pdfdocument_detail'),
    url(r'^(?P<pk>\d+)/save/$', PDFDocumentSaveView.as_view(), name='pdfdocument_save'),
    url(r'^(?P<pk>\d+)/feature/(?P<slug>[-\w]+)/$', PDFDocumentFeatureView.as_view(), name='pdfdocument_feature'),
    url(r'^(?P<pk>\d+)/edit/$', PDFDocumentUpdateView.as_view(), name='pdfdocument_update'),
    url(r'^new/$', PDFDocumentCreateView.as_view(), name='pdfdocument_create'),
    url(r'^rate/(?P<object_id>\d+)/(?P<score>\d+)/$', login_required(rate_pdfdocument), name='pdfdocument_rate'),
)



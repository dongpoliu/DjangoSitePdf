# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from .views import *
from profiles.views import UserUpdateView, UserProfileUpdateView
from django.contrib import admin
from profiles.models import UserProfile
from django.views.generic import RedirectView
from .sitemaps import sitemaps
from pdf.models import PDFDocument, Category
from pdf import views
from django.contrib.auth.models import User
#from rest_framework import routers, serializers, viewsets

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='page_home'),
    url(r'^explore/$', explore_home, name='explore_home'),
    url(r'^admin/$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^manage/', include(admin.site.urls)),    
    url(r'^explore/pdfdocument/all/$', RecentPDFDocumentListView.as_view(), name='explore_recent_pdfdocuments'),
    url(r'^explore/domain/all/$', PopularDomainListView.as_view(), name='explore_all_domains'),
    url(r'^explore/category/all/$', PopularCategoryListView.as_view(), name='explore_all_categories'),
    url(r'^accounts/settings/core/$', UserUpdateView.as_view(), name='user_update'),
    url(r'^accounts/settings/info/$', UserProfileUpdateView.as_view(), name='userprofile_update'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns('',
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^pdfdocument/', include('pdf.urls')),
    url(r'^pdfdocument/(?P<pk>\d+)/$', views.PDFDocumentDetailView.as_view(), name='pdfdocument_detail'),   
    #url(r'^resource/', include('resources.urls')),
    url(r'^profile/', include('profiles.urls')),
    #url(r'^search/', include('haystack.urls')),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='page_about'),
    url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='page_contact'),
    url(r'^guidelines/$', 'flatpage', {'url': '/guidelines/'}, name='page_guidelines'),
    url(r'^license/$', 'flatpage', {'url': '/license/'}, name='page_license'),
)

urlpatterns += patterns('',
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

################### OR #####################
# You adjust each app urls according to your preferences
# urlpatterns += patterns('',
#     # Doorsale apps urls
#     url(r'^', include('doorsale.catalog.urls')),
#     url(r'^accounts/', include('doorsale.accounts.urls')),
#     url(r'^sales/', include('doorsale.sales.urls')),
#     url(r'^payments/', include('doorsale.payments.urls')),
#     url(r'^pages/', include('doorsale.pages.urls'))
# )

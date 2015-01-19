# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from collections import Counter
from urlparse import urlparse
from django.views.generic import TemplateView, ListView
from braces.views import SetHeadlineMixin
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from pdf.models import Category, PDFDocument
from django.db.models import Count
from django.contrib.auth.models import User

def popular_domains_mixin(number='more'):
    pdfdocuments = PDFDocument.objects.all()
    cnt = Counter()
    domains = []
    for pdfdocument in pdfdocuments:
        domains.append(urlparse(pdfdocument.url)[1])
    for domain in domains:
        cnt[domain] += 1
    if number=='less':
        return cnt.most_common(5)
    else:
        return cnt.most_common()
    
class PopularCategoryListView(SetHeadlineMixin, ListView):
    context_object_name = 'popular_categories'
    template_name = 'explore/explore_all_categories.html'
    headline = 'Categories by Popularity'

    def get_queryset(self):
        return Category.objects.annotate(no_of_pdfdocuments=Count('pdfdocument')).order_by('-no_of_pdfdocuments')


class PopularDomainListView(SetHeadlineMixin, ListView):
    context_object_name = 'popular_domains'
    template_name = 'explore/explore_all_domains.html'
    headline = 'All Domains by Popularity'

    def get_queryset(self):
        return popular_domains_mixin()


class RecentPDFDocumentListView(SetHeadlineMixin, ListView):
    context_object_name = 'pdfdocuments'
    template_name = 'explore/explore_all_recent_pdfdocuments.html'
    headline = 'Recent PDFDocument'

    def get_queryset(self):
        return PDFDocument.objects.all().order_by('-created_at')[:50]


def explore_home(request):
    active_users = User.objects.annotate(no_of_pdfdocuments=Count('pdfdocument')).order_by('-no_of_pdfdocuments')
    popular_categories = Category.objects.annotate(no_of_pdfdocuments=Count('pdfdocument')).order_by('-no_of_pdfdocuments')

    recent_pdfdocuments = PDFDocument.objects.all().order_by('-created_at')[:5]
    popular_pdfdocuments = PDFDocument.objects.all().order_by('-rating_votes')[:5]

    ctx = {
            'active_users': active_users[:4],
            'popular_categories': popular_categories[:5],
            'popular_domains': popular_domains_mixin(number='less'),
            'recent_pdfdocuments': recent_pdfdocuments,
            'popular_pdfdocuments': popular_pdfdocuments,
            'headline': 'Explore'
    }
    return render_to_response('explore/explore_home.html', ctx, context_instance=RequestContext(request))


class ExploreView(SetHeadlineMixin, TemplateView):
    template_name = 'coming_soon.html'
    headline = 'Explore - Coming Soon'


class HomeView(SetHeadlineMixin, TemplateView):
    template_name = 'index.html'
    headline = 'Welcome'


class AboutView(SetHeadlineMixin, TemplateView):
    template_name = 'about.html'
    headline = 'About Us'


class ContactView(SetHeadlineMixin, TemplateView):
    template_name = 'contact.html'
    headline = 'Contact Us'


class GuidelinesView(SetHeadlineMixin, TemplateView):
    template_name = 'guidelines.html'
    headline = 'Guidelines'
class BaseView(TemplateView):
    """
    Base view for all Doorsale views

    Provide site context variables from settings and apply decoractors to views
    """
    # Pipeline CSS style package name
    style_name = 'base'

    # Base template to extend in drived views
    base_template_name = 'doorsale/base.html'

    # Decorators applied to generated view
    decorators = []

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        # Settings context data for base template
        context['request'] = self.request
        context['style_name'] = self.style_name
        context['base_template_name'] = self.base_template_name
        context['SITE_NAME'] = self.get_config('SITE_NAME')
        context['SITE_TITLE'] = self.get_config('SITE_TITLE')
        context['SITE_DESCRIPTION'] = self.get_config('SITE_DESCRIPTION')
        context['COPYRIGHT'] = self.get_config('COPYRIGHT')
        context['SUPPORT_EMAIL'] = self.get_config('SUPPORT_EMAIL')

        if hasattr(self, 'page_title'):
            context['page_title'] = self.page_title

        return context

    @classmethod
    def get_decorators(cls):
        """
        Returns list of decorators defined as attribute of class

        Generic base views should override get_decorators method instead of defining decorators attribute
        """
        return cls.decorators

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Returns view function

        Decorators will be applied defined at class level
        """
        view = super(BaseView, cls).as_view(**initkwargs)

        # Applying decorators to generated view
        for decorator in cls.get_decorators():
            view = decorator(view)

        return view

    #@staticmethod
    #def get_config(name):
        #return SysConfig.get_config(name)

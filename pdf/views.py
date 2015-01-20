# -*- coding: UTF-8 -*-
from datetime import datetime
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured,ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from main.views import BaseView
from pdf.models import Category, PDFDocument,PDFDocumenttype

from collections import Counter
from urlparse import urlparse
from braces.views import SetHeadlineMixin
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.utils.datastructures import SortedDict
from django.views.generic import View,TemplateView, ListView, DetailView, CreateView, UpdateView, RedirectView
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin
from djangoratings.views import AddRatingView
from django.contrib.contenttypes.models import ContentType
from profiles.models import SavedPDFDocument, CategoryFollow

from .forms import PDFDocumentCreateForm, PDFDocumentUpdateForm, CategoryCreateForm, CategoryUpdateForm,PDFDocumentForm


#add restful framework part
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import PDFDocument
from .serializers import PDFDocumentSerializer


@login_required
def doc_upload(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.date_uploaded = datetime.utcnow()
            doc.save()
            process_file.delay(doc)
            return HttpResponseRedirect(reverse('pdfdocument_list'))
    else:
        form = PDFDocumentForm()
    return render_to_response('pdf/upload.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def doc_list(request):
    context = {'pdfs': PDFDocument.objects.filter(user=request.user)}
    return render_to_response('pdf/list.html', context, context_instance=RequestContext(request))


@login_required
def doc_detail(request, uuid):
    context = {'pdf': PDFDocument.objects.get(uuid=uuid)}
    return render_to_response('pdf/detail.html', context, context_instance=RequestContext(request))

def pdfdocument_home(request):
    categories = Category.objects.filter(pdfdocument__name__isnull=False).distinct().order_by('name')

    #Check various session values for user details and show appropriate info
    #if request.session.get('no_name', False):
    #    messages.info(request, 'Please fill in your profile details by going to your account settings.')
    #    request.session['no_name'] = False

    if request.session.get('no_category', False):
        messages.warning(request, 'It seems you are not following any category. Follow categories by clicking on it below and get personalized recommendations')
        request.session['no_category'] = False

    ctx = {
            'categories': categories,
        }
    return render_to_response('pdfs/pdfdocument_home.html', ctx, context_instance=RequestContext(request))

def category_home(request, slug):
    current_category = get_object_or_404(Category, slug=slug)
    headline = """Learn """ + unicode(current_category.name).capitalize() + """ - from the best tutorials and online courses"""
    categories = Category.objects.filter(pdfdocument__name__isnull=False).distinct().order_by('name')

    ctx = {
        'current_category': current_category,
        'headline': headline,
        'categories': categories
    }

    pdfdocumenttypes = []
    pdfdocument_types = PDFDocumentType.objects.all().order_by('name')
    for pdfdocument_type in pdfdocument_types:
        try:
            result = FeaturedPDFDocument.objects.get(category=current_category, pdfdocument_type=pdfdocument_type)
            pdfdocumenttypes.append((result.pdfdocument_type.slug, result.pdfdocument))
        except FeaturedPDFDocument.DoesNotExist:
            result = current_category.pdfdocument_set.filter(pdfdocument_type=pdfdocument_type).order_by('-rating_votes')
            if len(result) > 0:
                pdfdocumenttypes.append((result[0].pdfdocument_type.slug, result[0]))
    ctx['pdfdocumenttypes'] = SortedDict(pdfdocumenttypes)

    return render_to_response('pdfs/category_home.html', ctx, context_instance=RequestContext(request))


def rate_pdfdocument(request, object_id, score):
    model = 'pdfdocument'
    app_label = 'pdfdocuments'
    field_name ='rating'
    try:
        content_type = ContentType.objects.get(model=model, app_label=app_label)
    except ContentType.DoesNotExist:
        raise Http404('Invalid `model` or `app_label`.')
    params = {
            'content_type_id': content_type.id,
            'object_id': object_id,
            'field_name': field_name,
            'score': score,
        }
    response = AddRatingView()(request, **params)
    if response.status_code == 200:
        if response.content == 'Vote recorded.':
            messages.success(request, 'Thanks, Your Vote is recorded')
    else:
        messages.error(request, 'Sorry, Something went wrong')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class PDFDocumentSaveView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, pk):
        pdfdocument = get_object_or_404(PDFDocument, pk=pk)
        SavedPDFDocument.objects.get_or_create(user=self.request.user, pdfdocument=pdfdocument)
        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return reverse_lazy('pdfdocument_detail', kwargs={'pk':pk})


class PDFDocumentFeatureView(LoginRequiredMixin, RedirectView):
    permanent = False
    permission_required = 'pdfdocuments.change_featuredpdfdocument'
    return_403 = True

    def get_redirect_url(self, pk, slug):
        pdfdocument = get_object_or_404(PDFDocument, pk=pk)
        category = get_object_or_404(Category, slug=slug)
        pdfdocument.make_featured(category=category)
        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        else:
            return reverse_lazy('pdfdocument_detail', kwargs={'pk':pk})


class SidebarMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SidebarMixin, self).get_context_data(**kwargs)
        categories = Category.objects.filter(pdfdocument__name__isnull=False).distinct().order_by('name')
        context['categories'] = categories
        return context


class PDFDocumentAllListView(SetHeadlineMixin, SidebarMixin, ListView):
    context_object_name = 'pdfdocuments'
    template_name = 'pdfs/pdfdocument_list.html'
    paginate_by = 12

    def get_queryset(self):
        level_to_get = None
        if 'level' in self.request.GET:
            level_to_get = self.request.GET['level']
        pdfdocuments = PDFDocument.objects.all()
        if level_to_get:
            pdfdocuments = pdfdocuments.filter(level=level_to_get)
        self.headline = 'All Books'
        return pdfdocuments


class CategoryFollowView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, slug):
        category = get_object_or_404(Category, slug=slug)
        try:
            tf = CategoryFollow.objects.get(user=self.request.user, category=category)
            tf.delete()
            messages.success(self.request, 'You have stopped following this category.')
        except CategoryFollow.DoesNotExist:
            CategoryFollow.objects.create(user=self.request.user, category=category)
            messages.success(self.request, 'You are now following this category.')
        return reverse_lazy('pdfdocument_category_home', kwargs={'slug':slug})

def category_home(request, slug):
    current_category = get_object_or_404(Category, slug=slug)
    headline = """Learn """ + unicode(current_category.name).capitalize() + """ - from the best tutorials and online courses"""
    categories = Category.objects.filter(pdfdocument__name__isnull=False).distinct().order_by('name')

    ctx = {
        'current_category': current_category,
        'headline': headline,
        'categories': categories
    }

    pdfdocumenttypes = []
    pdfdocument_types = PDFDocumenttype.objects.all().order_by('name')
    #for pdfdocument_type in pdfdocument_types:
        #try:
            #result = FeaturedPDFDocument.objects.get(category=current_category, pdfdocument_type=pdfdocument_type)
            #pdfdocumenttypes.append((result.pdfdocument_type.slug, result.pdfdocument))
        #except FeaturedPDFDocument.DoesNotExist:
            #result = current_category.pdfdocument_set.filter(pdfdocument_type=pdfdocument_type).order_by('-rating_votes')
            #if len(result) > 0:
                #pdfdocumenttypes.append((result[0].pdfdocument_type.slug, result[0]))
    ctx['pdfdocumenttypes'] = SortedDict(pdfdocumenttypes)

    return render_to_response('pdfs/category_home.html', ctx, context_instance=RequestContext(request))


class PDFDocumentCategoryListView(SetHeadlineMixin, SidebarMixin, ListView):
    context_object_name = 'pdfdocuments'
    template_name = 'pdfs/pdfdocument_list.html'
    paginate_by = 12

    def get_queryset(self):
        level_to_get = None
        pdfdocument_type = None
        slug = self.kwargs['slug']
        try:
            pdfdocument_type = self.kwargs['pdfdocument_type']
        except KeyError:
            pass
        if 'level' in self.request.GET:
            level_to_get = self.request.GET['level']
        category = get_object_or_404(Category, slug=slug)
        pdfdocuments = category.pdfdocument_set.all()
        self.headline = 'All ' + unicode(category.name).capitalize() +' PDFDocuments'
        if pdfdocument_type:
            pdfdocument_type = get_object_or_404(PDFDocumenttype, slug=pdfdocument_type)
            pdfdocuments = pdfdocuments.filter(pdfdocument_type=pdfdocument_type)
            self.headline = unicode(category.name).capitalize() +' PDFDocuments' + ' (' + unicode(pdfdocument_type.name) + 's)'
        if level_to_get and level_to_get != 'all':
            pdfdocuments = pdfdocuments.filter(level=level_to_get)
        return pdfdocuments

    def get_context_data(self, **kwargs):
        context = super(PDFDocumentCategoryListView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['current_category'] = category
        return context


class PDFDocumentDetailView(SetHeadlineMixin, SidebarMixin, DetailView):
    model = PDFDocument
    context_object_name = 'pdfdocument'
    template_name = 'pdfs/pdfdocument_detail.html'

    def get_object(self):
        pdfdocument = super(PDFDocumentDetailView, self).get_object()
        self.headline = unicode(pdfdocument.name) + """ (""" + unicode(pdfdocument.pdfdocument_type) + """) | PDFDocument"""
        return pdfdocument

    def get_context_data(self, **kwargs):
        context = super(PDFDocumentDetailView, self).get_context_data(**kwargs)
        return context


class PDFDocumentCreateView(LoginRequiredMixin, SetHeadlineMixin, SidebarMixin, CreateView):
    form_class = PDFDocumentCreateForm
    template_name = 'pdfs/pdfdocument_form.html'
    model = PDFDocument
    headline = 'Add new Chinese Picture Book'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(PDFDocumentCreateView, self).form_valid(form)


class PDFDocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SetHeadlineMixin, SidebarMixin, UpdateView):
    form_class = PDFDocumentUpdateForm
    model = PDFDocument
    headline = 'Edit PDF'
    permission_required = 'pdfdocuments.change_pdfdocument'
    return_403 = True


class CategoryCreateView(SetHeadlineMixin, SidebarMixin, CreateView):
    form_class = CategoryCreateForm
    template_name = 'pdfs/category_form.html'
    permission_required = 'pdfdocuments.add_category'
    headline = 'Create New Category'


class CategoryUpdateView(PermissionRequiredMixin, SetHeadlineMixin, SidebarMixin, UpdateView):
    form_class = CategoryUpdateForm
    model = Category
    template_name = 'pdfs/category_form.html'
    permission_required = 'pdfdocuments.change_category'
    render_403 = True
    return_403 = True
    headline = 'Edit Category'

#add restful framework part
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def pdfdocument_list(request):
    """
    List all code PDFDocument, or create a new PDFDocument.
    """
    if request.method == 'GET':
        pdfdocument = PDFDocument.objects.all()
        serializer = PDFDocumentSerializer(pdfdocuments, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PDFDocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def pdfdocument_detail(request, pk):
    """
    Retrieve, update or delete a code PDFDocument.
    """
    try:
        pdfdocument = PDFDocument.objects.get(pk=pk)
    except PDFDocument.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PDFDocumentSerializer(pdfdocument)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PDFDocumentSerializer(pdfdocument, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        pdfdocument.delete()
        return HttpResponse(status=204)
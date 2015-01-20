# -*- coding: UTF-8 -*-
import os

from datetime import datetime
from django.conf import settings
#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from djangoratings.fields import RatingField
from main.utils import unique_slugify
from django.template.defaultfilters import slugify

DEFAULT_PATH = os.path.join(settings.MEDIA_ROOT, "uploads")
UPLOAD_PATH = getattr(settings, "PDF_UPLOAD_PATH", DEFAULT_PATH)

class Category(models.Model):
    """
    Represents a Category for Chinese Picture-Book
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='categories', null=True, blank=True)
    help_text = models.CharField(max_length=255, null=True, blank=True)
    official_website = models.URLField(null=True, blank=True)
   
    class Meta:
        ordering = ['name',]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pdfdocument_category_home', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.description and not self.help_text:
            self.help_text = self.description.replace("\n", " ")[:220]
        super(Category, self).save(*args, **kwargs)

class PDFDocumenttype(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=255)
    help_text = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=20, default='purple', unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pdfdocument_list', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(PDFDocumenttype, self).save(*args, **kwargs)

class PDFDocument(models.Model):
    """
    model for an uploaded PDF document.
    """
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=255,blank=True, default='')
    #url = models.URLField(unique=True)
    help_text = models.CharField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField(Category)
    description = models.TextField(null=True, blank=True)
    pdfdocument_type = models.ForeignKey(PDFDocumenttype)    
    created_by = models.ForeignKey(User,default='1')
    rating = RatingField(range=5, weight=10, use_cookies=True, allow_delete=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False,default='2015-01-15')
    updated_at = models.DateTimeField(auto_now=True, editable=False)    
        
    thumbnail = models.ImageField(upload_to='PDFDocuments', null=True, blank=True)
    local_document = models.FileField(_("Local Document"), null=True, blank=True, upload_to=UPLOAD_PATH)
    pages = models.IntegerField(_("Number of Pages in Document"), null=True, blank=True)
    show = models.BooleanField(default=True)    
    
    class Meta:
        ordering = ['id',]
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pdfdocument_detail', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.description and not self.help_text:
            self.help_text = self.description.replace("\n", " ")[:220]
        super(PDFDocument, self).save(*args, **kwargs)
      
class FeaturedPDFDocument(models.Model):                        
    category= models.ForeignKey(Category)
    pdfdocument_type = models.ForeignKey(PDFDocumenttype)
    pdfdocument = models.ForeignKey(PDFDocument)

    class Meta:
        unique_together = ('category', 'pdfdocument_type')

    def __unicode__(self):
        return '%s - %s' %(self.category, self.pdfdocument_type)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.pdfdocument_type != self.pdfdocument.pdfdocument_type:
            raise ValidationError("Selected pdfdocument type does not match with given pdfdocument's type.")
        if not self.category in self.pdfdocument.categories.all():
            raise ValidationError("Selected pdfdocument does not have given category.")

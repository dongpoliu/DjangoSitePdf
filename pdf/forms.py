# -*- coding: UTF-8 -*-

import os
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import PDFDocument,Category

class PDFDocumentCreateForm(ModelForm):
    class Meta:
        model = PDFDocument
        exclude = ('slug', 'help_text','created_by',)

class PDFDocumentUpdateForm(ModelForm):
    class Meta:
        model = PDFDocument
        exclude = ('slug', 'help_text')

class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

class CategoryUpdateForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)


class PDFDocumentValidationError(forms.ValidationError):
    def __init__(self):
        msg = _(u'Only PDF files are valid uploads.')
        super(DocumentValidationError, self).__init__(msg)


class PDFDocumentField(forms.FileField):
    """A validating PDF document upload field"""

    def clean(self, data, initial=None):
        f = super(DocumentField, self).clean(data, initial)
        ext = os.path.splitext(f.name)[1][1:].lower()
        if ext == 'pdf' and f.content_type == 'application/pdf':
            return f
        raise DocumentValidationError()


class PDFDocumentForm(forms.ModelForm):
    local_document = forms.FileField(
        label='Select a PDF file',
        help_text='max. 42 megabytes'
    )
    class Meta:
        model = PDFDocument
        fields = ('name', 'slug', 'pages','thumbnail','local_document',)




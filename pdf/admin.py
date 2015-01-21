# -*- coding: UTF-8 -*-
from django.contrib import admin
from pdf.models import PDFDocument,Category,PDFDocumenttype

class PDFDocumenttypeAdmin(admin.ModelAdmin):
    list_display=('name', 'color',)
    prepopulated_fields = {'slug': ['name',]}


class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'pages','thumbnail','local_document',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('id', 'name', 'description',)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name',)
    prepopulated_fields = {'slug': ['name',]}

admin.site.register(PDFDocument, PDFDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PDFDocumenttype, PDFDocumenttypeAdmin)

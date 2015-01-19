from django.contrib.sitemaps import GenericSitemap
from pdf.models import Category,PDFDocument

pdfdocument_dict = {
        'queryset': PDFDocument.objects.filter(show=True),
        'date_field': 'updated_at',
}
category_dict = {
        'queryset': Category.objects.all(),
}

sitemaps = {
    'category': GenericSitemap(category_dict, priority=0.8),
    'pdfdocument': GenericSitemap(pdfdocument_dict, priority=0.6),
}


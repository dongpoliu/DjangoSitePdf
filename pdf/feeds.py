from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from .models import PDFDocument, Category

class RecentPDFDocumentsRss(Feed):
    title = "Recent PDFDocuments "
    link = "/pdfdocument/"
    description = "Provides feed for recent pdfdocuments shared"
    description_template = "feeds/pdfdocuments.html"

    def items(self):
        return PDFDocument.objects.order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title


class RecentPDFDocumentsAtom(RecentPDFDocumentsRss):
    feed_type = Atom1Feed
    subtitle = RecentPDFDocumentsRss.description


class CategoryRecentPDFDocumentsRss(Feed):
    description_template = "feeds/pdfdocuments.html"

    def get_object(self, request, category_slug):
        return get_object_or_404(Category, slug=category_slug)

    def title(self, obj):
        return "Recent pdfdocuments for %s" %obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "feed for recent pdfdocuments shared for %s" %obj.name

    def items(self, obj):
        return obj.pdfdocument_set.all().order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title


class CategoryRecentPDFDocumentsAtom(CategoryRecentPDFDocumentsRss):
    feed_type = Atom1Feed
    subtitle = CategoryRecentPDFDocumentsRss.description

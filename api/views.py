from django.contrib.auth.models import User
from pdf.models import PDFDocument, Category
from api.serializers import UserSerializer, CategorySerializer, PDFDocumentSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PDFDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer

from django.forms import widgets
from rest_framework import serializers
from .models import PDFDocument


class PDFDocumentSerializer(serializers.Serializer):
    class Meta:
        model = PDFDocument
        fields = ('id', 'name', 'pages')
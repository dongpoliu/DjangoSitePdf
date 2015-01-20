from django.forms import widgets
from rest_framework import serializers
from .models import PDFDocument


class PDFSerializer(serializers.Serializer):
    class Meta:
        model = PDFDocument
        fields = ('id', 'name', 'categories', 'created_by', 'thumbnail', 'pages')
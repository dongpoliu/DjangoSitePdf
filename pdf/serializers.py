from django.forms import widgets
from rest_framework import serializers
from .models import PDFDocument


class PDFSerializer(serializers.Serializer):
    class Meta:
        model = PDFDocument
        fields = ('id', 'name', 'code', 'linenos', 'language', 'style')
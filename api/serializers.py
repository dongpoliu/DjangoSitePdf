# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from pdf.models import PDFDocument, Category
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
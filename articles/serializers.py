from rest_framework import serializers
from .models import Article, Opinion

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'titre', 'contenu']

class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ['id', 'user_id', 'article', 'opinion', 'date_response']

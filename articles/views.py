import json
from rest_framework import viewsets, status
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import Article, Opinion, FinalVote  # Assurez-vous que FinalVote est bien défini
from .serializers import ArticleSerializer, OpinionSerializer
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Vues basées sur ViewSet pour les articles et les opinions
class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

class OpinionViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = OpinionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue JSON pour la liste des articles
class ArticleListView(View):
    def get(self, request):
        articles = list(Article.objects.values())
        return JsonResponse({'articles': articles})

# Vue JSON pour les détails d'un article
class ArticleDetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return JsonResponse({
            'id': article.id,
            'titre': article.titre,
            'contenu': article.contenu
        })

@method_decorator(csrf_exempt, name='dispatch')
class OpinionCreateView(View):
    def post(self, request):
        try:
            # Tente de charger les données JSON depuis le corps de la requête
            data = json.loads(request.body)
            user_id = data.get('user_id')
            article_id = data.get('article_id')
            opinion = data.get('opinion')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Les données JSON sont invalides'}, status=400)

        if not all([user_id, article_id, opinion is not None]):
            return JsonResponse({'error': 'Des champs sont manquants'}, status=400)

        # Crée une nouvelle opinion
        new_opinion = Opinion.objects.create(user_id=user_id, article_id=article_id, opinion=opinion)
        return JsonResponse({'message': 'Opinion enregistrée avec succès !', 'opinion_id': new_opinion.id})

# Vue pour obtenir les statistiques de l'utilisateur
@api_view(['GET'])
def user_statistics(request, user_id):
    opinions = Opinion.objects.filter(user_id=user_id)
    total_articles = Article.objects.count()

    if total_articles == 0:
        return Response({'error': 'Aucun article trouvé'}, status=400)

    agrees = opinions.filter(opinion=True).count()  # Utilise True pour les opinions d'accord
    disagrees = total_articles - agrees

    data = {
        'agree_percentage': round((agrees / total_articles) * 100, 2),
        'disagree_percentage': round((disagrees / total_articles) * 100, 2),
    }
    return Response(data)


# Vue pour enregistrer le vote final et le commentaire
@api_view(['POST'])
def final_vote(request, user_id):
    vote = request.data.get('vote')
    comment = request.data.get('comment')
    if not vote:
        return Response({"error": "Le vote est requis."}, status=status.HTTP_400_BAD_REQUEST)
    FinalVote.objects.create(user_id=user_id, vote=vote, comment=comment)
    return Response({"message": "Votre vote final a été enregistré."})

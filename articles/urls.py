from django.urls import path
from . import views  # Importer les vues de l'application 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),  # Liste des articles
    path('opinion/', views.OpinionCreateView.as_view(), name='opinion-create'),  # Création d'une opinion
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),  # Détail d'un article spécifique
    path('user_statistics/<int:user_id>/', views.user_statistics, name='user-statistics'),  # Route pour user_statistics
    path('final_vote/<int:user_id>/', views.final_vote, name='final-vote'),  # URL pour le vote final
]


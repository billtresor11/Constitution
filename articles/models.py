from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField()

    def __str__(self):
        return self.titre

class Opinion(models.Model):
    user_id = models.IntegerField()  # Ou utiliser un modèle User si nécessaire
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    opinion = models.BooleanField()  # True pour "D'accord", False pour "Pas d'accord"
    date_response = models.DateTimeField(auto_now_add=True)


class FinalVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class FinalVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associe le vote à un utilisateur spécifique
    vote = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])  # Vote final (Oui ou Non)
    comment = models.TextField(blank=True, null=True)  # Champ pour le commentaire de l'utilisateur
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'enregistrement du vote

    def __str__(self):
        return f"Vote de {self.user.username}: {self.vote}"
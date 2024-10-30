from django.contrib import admin
from django.urls import path, include  # Importer 'include' pour inclure les URLs d'autres applications

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/articles/', include('articles.urls')),  # Inclut les URLs de l'application 'articles'
    path('api/', include('articles.urls')),  # Cela inclut toutes les routes de articles sous /api/

]




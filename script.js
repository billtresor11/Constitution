let currentArticleId = 1; // ID de l'article actuel
let totalArticles = 4; // Nombre total d'articles (à ajuster)

function loadArticle(articleId) {
    fetch(`http://127.0.0.1:8000/api/articles/${articleId}/`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('articleTitle').innerText = data.titre;
                document.getElementById('articleContent').innerText = data.contenu;
            } else {
                showFinalNotification(); // Afficher les statistiques si aucun article n’est trouvé
            }
        })
        .catch(error => console.error("Erreur lors du chargement de l'article :", error));
}

function submitOpinion(isAgree) {
    fetch('http://127.0.0.1:8000/api/opinion/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: 1,  // Remplace par l'ID utilisateur réel
            article_id: currentArticleId,
            opinion: isAgree  // true pour "D'accord", false pour "Pas d'accord"
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Réponse de l'opinion :", data);
            if (data.message) {  // Si l'opinion est bien enregistrée
                currentArticleId++;  // Passe à l'article suivant
                if (currentArticleId <= totalArticles) {
                    loadArticle(currentArticleId);  // Charge l'article suivant
                } else {
                    showFinalNotification();  // Affiche les statistiques à la fin
                }
            }
        })
        .catch(error => console.error("Erreur lors de l'enregistrement de l'opinion :", error));
}

function showFinalNotification() {
    // Masque les éléments de l'article et les boutons
    document.getElementById('articleTitle').style.display = 'none';
    document.getElementById('articleContent').style.display = 'none';
    document.getElementById('agreeButton').style.display = 'none';
    document.getElementById('disagreeButton').style.display = 'none';

    // Affiche le résumé des statistiques
    fetch(`http://127.0.0.1:8000/api/user_statistics/1/`)  // Remplace 1 par l'ID utilisateur réel
        .then(response => response.json())
        .then(data => {
            document.getElementById('summaryTitle').innerText = 'Résumé de l’opinion global';  // Texte de titre
            document.getElementById('agreePercentage').innerText = `Pourcentage d'accord : ${data.agree_percentage}%`;
            document.getElementById('disagreePercentage').innerText = `Pourcentage de désaccord : ${data.disagree_percentage}%`;
            document.getElementById('finalNotification').style.display = 'block';
        })
        .catch(error => console.error("Erreur lors de la récupération des statistiques :", error));

    document.getElementById('finalVoteForm').onsubmit = function(event) {
        event.preventDefault();
        const vote = document.querySelector('[name="vote"]').value;
        const comment = document.querySelector('[name="comment"]').value;

        fetch(`http://127.0.0.1:8000/api/final_vote/1/`, {  // Remplace 1 par l'ID utilisateur actuel
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ vote: vote, comment: comment })
        })
            .then(response => response.json())
            .then(data => {
                // Masque tous les éléments après le vote final
                document.getElementById('finalNotification').style.display = 'none';
                document.getElementById('finalVoteForm').style.display = 'none';

                // Affiche un message de remerciement
                const thankYouMessage = document.createElement('p');
                thankYouMessage.innerText = "Merci d'avoir partagé votre avis. Nous avons bien pris en compte votre participation.";
                document.body.appendChild(thankYouMessage);
            })
            .catch(error => console.error("Erreur lors de l'enregistrement du vote final :", error));
    };




}

// Gestion des clics sur les boutons
document.getElementById('agreeButton').addEventListener('click', () => submitOpinion(true));
document.getElementById('disagreeButton').addEventListener('click', () => submitOpinion(false));

// Charger le premier article au démarrage
loadArticle(currentArticleId);

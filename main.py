from plateforme import Plateforme
#test
if __name__ == '__main__':
    #Etape 1 : Initialisation de la plateforme
    p = Plateforme()
    p.charger_depuis_bdd()
    p.afficher_catalogue()
    #Etape 2 : connexion d'un utilisateur
    alice = p.trouver_utilisateur("alice92")
    alice.se_connecter("alice92", "hash1")

    criteres = {"sous_categorie": "Vestes", "couleur": "Bleu", "taille": "M"}

    alice = p.trouver_utilisateur("alice92")
    alice_acheteur = p.en_tant_que_acheteur(alice)
    resultats = alice_acheteur.rechercher_articles(p.articles, criteres)
    for article, score in resultats:
        print(f"{article.nom} — score: {score:.2f}")
    # Bob veut vendre
    bob = p.trouver_utilisateur("bob_style")
    bob_vendeur = p.en_tant_que_vendeur(bob)
    article = p.articles[0]
    bob_vendeur.mettre_en_vente(article)


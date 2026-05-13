from models.plateforme import Plateforme

if __name__ == '__main__':

    #Etape 1 : Initialisation de la plateforme
    p = Plateforme()
    p.charger_depuis_bdd()
    p.afficher_catalogue()
    #Etape 2 : connexion d'un utilisateur
    criteres = {"sous_categorie": "Vestes", "couleur": "Bleu", "taille": "M"}

    alice = p.trouver_utilisateur("alice92")
    alice.se_connecter("alice92", "hash1")
    alice_acheteur = p.en_tant_que_acheteur(alice)
    resultats = alice_acheteur.rechercher_articles(p.articles, criteres)
    for article, score in resultats:
        print(f"{article.nom} — score: {score:.2f}")
    if resultats:
        meilleur_article, score = resultats[0]
        statut = alice_acheteur.faire_offre(meilleur_article, prix_propose=10)
        print(f"\nOffre de 30€ sur {meilleur_article.nom} → {statut}")

"""
p.creer_utilisateur("nouveau_user", "Dupont", "Jean", "jean@mail.com", "motdepasse123")
jean = p.trouver_utilisateur("nouveau_user")
print(f"Nouvel utilisateur : {jean.pseudo}, id : {jean.id}")
"""

# Bob veut vendre
bob = p.trouver_utilisateur("bob_style")
bob_vendeur = p.en_tant_que_vendeur(bob)
from models.article import Vetement

# Bob crée un nouvel article from scratch
nouveau_article = Vetement(
    id=21,
    nom="Doudoune North Face",
    description="Doudoune noire, très chaude, portée un hiver",
    categorie="Vêtements",
    prix_vendeur=120.0,
    prix_min=85.0,
    etat="tres_bon",
    id_vendeur=bob.id,
    date_publication="2026-05-11",
    photo="doudoune_tnf.jpg",
    vendu=0,
    sous_categorie="Manteaux",
    genre="Homme",
    taille="L",
    couleur="Noir",
    marque="The North Face",
    matiere="Nylon"
)

# Bob le met en vente
bob_vendeur.mettre_en_vente(nouveau_article)

# Ajout au catalogue de la plateforme
p.ajouter_article(nouveau_article)

# Vérification
print(f"\nNouvel article : {nouveau_article.nom} — {nouveau_article.prix_vendeur}€")
vendu, en_vente = bob_vendeur.mes_articles()
print(f"Articles de Bob : {len(en_vente)} en vente, {len(vendu)} vendus")
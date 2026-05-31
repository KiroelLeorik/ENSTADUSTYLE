""" ----------- Author : LARDILLIER Léo -------------

Ce main représente la console à partir de laquelle toutes les opérations sont effectuées.
"""

from models.plateforme import Plateforme
from models.article import Vetement


def init_plateforme() -> Plateforme:
    """Initialise et charge la plateforme depuis la BDD."""
    p = Plateforme()
    p.charger_depuis_bdd()
    return p


def demo_recherche(p: Plateforme) -> None:
    """Démontre la recherche d'articles et le matching acheteur/vendeur."""
    # Connexion
    alice = p.authentifier_utilisateur("alice92", "alice1234")
    alice_acheteur = p.en_tant_que_acheteur(alice)

    # Recherche
    criteres = {"sous_categorie": "Vestes", "couleur": "Bleu", "taille": "M"}
    resultats = alice_acheteur.rechercher_articles(p.articles, criteres)
    print("\n--- Résultats de recherche ---")
    for article, score in resultats:
        print(f"  {article.nom} — score: {score:.2f}")

    # Offre sur le meilleur résultat
    if resultats:
        meilleur_article, score = resultats[0]
        statut = alice_acheteur.faire_offre(meilleur_article, prix_propose=10)
        print(f"\nOffre de 10€ sur {meilleur_article.nom} → {statut}")
    p.deconnecter_utilisateur()


def demo_creation_utilisateur(p: Plateforme) -> None:
    """Démontre la création d'un nouvel utilisateur."""
    p.creer_utilisateur("nouveau_user", "Dupont", "Jean", "jean@mail.com", "motdepasse123")
    jean = p.trouver_utilisateur("nouveau_user")
    if jean:
        print(f"\nNouvel utilisateur : {jean.pseudo}, id : {jean.id}")


def demo_mise_en_vente(p: Plateforme) -> None:
    """Démontre la mise en vente d'un article par un vendeur."""
    # Connexion de Bob
    bob = p.authentifier_utilisateur("bob_style", "bobstyle99")
    bob_vendeur = p.en_tant_que_vendeur(bob)

    # Création d'un nouvel article
    nouveau_article = Vetement(
        id=None,
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

    # Mise en vente
    print("\n--- Mise en vente ---")
    print("Article mis en vente ?", bob_vendeur.mettre_en_vente(nouveau_article))
    p.ajouter_article(nouveau_article)
    print(f"Nouvel article : {nouveau_article.nom} — {nouveau_article.prix_vendeur}€")

    vendu, en_vente = bob_vendeur.mes_articles()
    print(f"Articles de Bob : {len(en_vente)} en vente, {len(vendu)} vendus")
    p.deconnecter_utilisateur()


def demo_recommandation(p: Plateforme) -> None:
    """Démontre l'algorithme de recommandation."""
    from services.recommandation import recommander

    alice = p.authentifier_utilisateur("alice92", "alice1234")
    alice_acheteur = p.en_tant_que_acheteur(alice)

    print(f"\n--- Favoris d'Alice ({len(alice_acheteur.favoris)}) ---")
    for f in alice_acheteur.favoris:
        print(f"  - {f.nom}")

    recommandations = recommander(alice_acheteur, p.articles)
    print(f"\n--- Recommandations pour Alice ---")
    for article, score in recommandations:
        print(f"  {article.nom} — score: {score:.2f}")
    p.deconnecter_utilisateur()


def demo_observer(p: Plateforme) -> None:
    """Démontre le pattern Observer — notification quand un article est mis en vente."""
    from services.observer import Observateur

    # Alice s'abonne aux vestes bleues taille M
    alice = p.authentifier_utilisateur("alice92", "alice1234")
    alice_acheteur = p.en_tant_que_acheteur(alice)
    p.deconnecter_utilisateur()

    obs = Observateur(alice_acheteur, {"taille": "M", "couleur": "Bleu"})
    p.abonner(obs)

    # Bob met en vente un article correspondant
    bob = p.authentifier_utilisateur("bob_style", "bobstyle99")
    bob_vendeur = p.en_tant_que_vendeur(bob)

    print("\n--- Test Observer ---")
    nouvel_article = Vetement(
        id=None,
        nom="Manteau en laine d'alpaga",
        description="Manteau de qualité exceptionnelle",
        categorie="Vêtements",
        prix_vendeur=120.0,
        prix_min=85.0,
        etat="neuf",
        id_vendeur=bob.id,
        date_publication="2026-05-30",
        photo="manteau_alpaga.jpg",
        vendu=0,
        sous_categorie="Manteaux",
        genre="Homme",
        taille="M",
        couleur="Bleu",
        marque="Sandro",
        matiere="Laine"
    )
    bob_vendeur.mettre_en_vente(nouvel_article)
    p.ajouter_article(nouvel_article)  # déclenche la notification
    p.deconnecter_utilisateur()

if __name__ == '__main__':
    p = init_plateforme()
    p.afficher_catalogue()

    # Décommente les fonctions que tu veux tester
    demo_recherche(p)
    # demo_creation_utilisateur(p)
    # demo_mise_en_vente(p)
    # demo_recommandation(p)
    # demo_observer(p)

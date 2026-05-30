#Test de l'algorithme de recommandation :
from services.recommendation import recommander
from models.plateforme import Plateforme

p = Plateforme()
p.charger_depuis_bdd()


def test_recommandation(p):
    alice = p.trouver_utilisateur("alice92")
    alice_acheteur = p.en_tant_que_acheteur(alice)

    print(f"Favoris d'Alice ({len(alice_acheteur.favoris)}) :")
    for f in alice_acheteur.favoris:
        print(f"  - {f.nom}")

    recommandations = recommander(alice_acheteur, p.articles)

    print(f"\nRecommandations pour Alice :")
    for article, score in recommandations:
        print(f"  {article.nom} — score: {score:.2f}")

#test_recommandation(p)

def test_observer(p):
    from services.observer import Observateur
    from models.article import Vetement
    alice = p.trouver_utilisateur("alice92")
    bob = p.trouver_utilisateur("bob_style")
    alice_acheteur = p.en_tant_que_acheteur(alice)
    bob_vendeur = p.en_tant_que_vendeur(bob)
    obs = Observateur(alice_acheteur, {"taille": "M", "couleur": "Bleu"})
    p.abonner(obs)

    # Quand Bob met un article en vente
    nouveau_article = Vetement(
        id=21,
        nom="Manteau en laine d'alpaga",
        description="Manteau de qualité exceptionnelle",
        categorie="Vêtements",
        prix_vendeur=120.0,
        prix_min=85.0,
        etat="neuf",
        id_vendeur=bob.id,
        date_publication="2026-05-11",
        photo="doudoune_tnf.jpg",
        vendu=0,
        sous_categorie="Manteaux",
        genre="Homme",
        taille="M",
        couleur="Bleu",
        marque="The North Face",
        matiere="Nylon"
    )
    p.ajouter_article(nouveau_article)  # → doit déclencher la notification pour Alice
test_observer(p)
for k in p._observateurs:
    print(k.acheteur.pseudo, k.criteres)
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

test_recommandation(p)
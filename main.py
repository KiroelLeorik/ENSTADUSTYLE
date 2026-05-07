# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models.utilisateur import Acheteur, Vendeur, Utilisateur
from models.transaction import Transaction
from models.article import Article, Vetement
from db.db import *
from services.recherche import rechercher
from services.matching import proposer_achat


if __name__ == '__main__':
    utilisateurs = get_all_utilisateurs()
    articles = get_all_articles()
    users = [Utilisateur(*u) for u in utilisateurs]
    vetements = [Vetement(*a) for a in articles]

    criteres = {'sous_categorie' : 'Vestes'}
    resultats = rechercher(vetements, criteres)

    for resultat in resultats:
        print(resultat.nom, resultat.prix_vendeur)
    if resultats:
        statut = proposer_achat(None, resultats[0], prix_acheteur=30)
        print(statut)

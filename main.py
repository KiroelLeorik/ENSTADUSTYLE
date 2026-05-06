# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models.utilisateur import Acheteur, Vendeur, Utilisateur
from models.transaction import Transaction
from models.article import Article, Vetement
from db.db import *

if __name__ == '__main__':
    utilisateurs = get_all_utilisateurs()
    articles = get_all_articles()
    for u in utilisateurs:
        user = Utilisateur(*u)
        print(user.pseudo, user.localisation)
    for a in articles:
        article = Vetement(*a)
        print(article.nom, article.prix_vendeur)
    pass
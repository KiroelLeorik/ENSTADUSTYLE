""" ----------- Author : GREGOIRE Louna ------------- """
from db.db import *

def proposer_achat(acheteur, article, prix_acheteur):
    prix_min = article.prix_min
    prix_vendeur = article.prix_vendeur

    if prix_acheteur >= prix_vendeur:
        statut = "acceptee"
        prix_final = prix_acheteur
        article.vendu = True
        update_article_vendu(article.id)
    elif prix_acheteur >= prix_min:
        statut = "negociation"
        prix_final = None
    else:
        statut = "refusee"
        prix_final = None

    insert_transaction(acheteur.id, article.id_vendeur, article.id, prix_acheteur, prix_final, statut)
    return statut
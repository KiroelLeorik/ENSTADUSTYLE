""" ----------- Author : GREGOIRE Louna ------------- """
from db.db import *

def proposer_achat(acheteur, article, prix_acheteur):
    prix_min = article.prix_min   #prix minimum auquel le vendeur peut vendre son article s'il y a négociation
    prix_vendeur = article.prix_vendeur  #prix affiché sur le site, prix auquel le vendeur veut vendre son article

    if prix_acheteur >= prix_vendeur: #si l'acheteur veut acheter le produit plus cher ou égal à celui proposé par le vendeur, la vente est acceptée l'article est vendue au prix de l'acheteur
        statut = "acceptee"
        prix_final = prix_acheteur
        article.vendu = True
        update_article_vendu(article.id)
    elif prix_acheteur >= prix_min:   #si le prix de l'acheteur est inferieur à celui sur le site mais superieur au prix minimum, il y a négociation
        statut = "negociation"
        prix_final = None
    else:
        statut = "refusee"   #sinon, l'article n'est pas acheté
        prix_final = None

    insert_transaction(acheteur.id, article.id_vendeur, article.id, prix_acheteur, prix_final, statut)
    return statut

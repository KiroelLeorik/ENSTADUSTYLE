""" ----------- Author : LARDILLIER Léo ------------- """

from datetime import datetime
from typing import Optional

class Transaction:
    """
    Représente une tentative d'achat entre un acheteur et un vendeur sur la plateforme.
    Enregistre le résultat de la négociation de prix ainsi que la date de l'opération.
    """

    def __init__(self, acheteur: "Acheteur", vendeur: "Vendeur", article: "Article",
                 prix_propose: float, prix_final: Optional[float], statut: str) -> None:
        """
        :param acheteur: instance de Acheteur ayant soumis l'offre
        :param vendeur: instance de Vendeur propriétaire de l'article
        :param article: instance de Article concerné par la transaction
        :param prix_propose: prix proposé par l'acheteur (en euros)
        :param prix_final: prix de vente définitif, ou None si la vente n'est pas conclue
        :param statut: résultat de la négociation ('acceptee', 'negociation' ou 'refusee')
        """
        self.acheteur = acheteur
        self.vendeur = vendeur
        self.article = article
        self.prix_propose = prix_propose
        self.prix_final = prix_final
        self.statut = statut
        self.date = datetime.now()

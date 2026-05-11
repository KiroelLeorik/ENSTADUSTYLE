from datetime import datetime

class Transaction:
    def __init__(self, acheteur, vendeur, article, prix_propose, prix_final, statut):
                """
        
        :param acheteur: 
        :param vendeur: 
        :param article: 
        :param prix_propose: 
        :param prix_final: 
        :param statut: 
        """
        self.acheteur = acheteur
        self.vendeur = vendeur
        self.article = article
        self.prix_propose = prix_propose
        self.prix_final = prix_final
        self.statut = statut
        self.date = datetime.now()

    def afficher_detail(self):
                """
        
        :return: 
        """
        print('Transaction effectuées')

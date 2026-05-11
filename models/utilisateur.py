class Utilisateur:
    def __init__(self, id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription):
            """
    
    :param self: 
    :param id: 
    :param pseudo: 
    :param nom: 
    :param prenom: 
    :param mail: 
    :param mot_de_passe: 
    :param est_pro: 
    :param evaluation: 
    :param localisation: 
    :param date_inscription: 
    :return: 
    """
        self.id = id
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.__mot_de_passe = mot_de_passe
        self.est_pro = est_pro
        self.evaluation = evaluation
        self.localisation = localisation
        self.date_inscription = date_inscription

    @property
    def mot_de_passe(self):
            """
    
    :param self: 
    :return: 
    """
        return self.__mot_de_passe

    @mot_de_passe.setter
    def mot_de_passe(self, nouveau_mdp):
            """
    
    :param self: 
    :param nouveau_mdp: 
    :return: 
    """
        if len(nouveau_mdp) < 6:
            print("Le nouveau mot de passe doit au moins contenir 6 caractères")
            return False
        self.__mot_de_passe = nouveau_mdp
        return True

    def set_mot_de_passe(self, ancien_mdp, nouveau_mdp):
            """
    
    :param self: 
    :param ancien_mdp: 
    :param nouveau_mdp: 
    :return: 
    """
        if ancien_mdp != self.__mot_de_passe:
            print("Ancien mot de passe incorrect")
            return False
        self.mot_de_passe = nouveau_mdp
        return True

    def se_connecter(self, pseudo, mdp):
            """
    
    :param self: 
    :param pseudo: 
    :param mdp: 
    :return: 
    """
        if pseudo != self.pseudo:
            print("Pseudo incorrect")
            return False
        if mdp != self.mot_de_passe:
            print("Mot de passe incorrect")
            return False
        print("Vous êtes connectés")
        return True

    def modifier_profil(self, pseudo=None, mail=None, localisation=None):
            """
    
    :param self: 
    :param pseudo: 
    :param mail: 
    :param localisation: 
    :return: 
    """

    # Met à jour les attributs du profil

    def afficher_profil(self):
                """
        
        :param self: 
        :return: 
        """
    # Retourne un résumé de l'utilisateur

class Vendeur(Utilisateur):
    def mettre_en_vente(self, article):
            """
    
    :param self: 
    :param article: 
    :return: 
    """
    # Ajoute un article à sa liste d'articles en vente

    def retirer_article(self, article):
            """
    
    :param self: 
    :param article: 
    :return: 
    """


    # Retire un article de la vente

    def mes_articles(self, tous_les_articles):


# Retourne ses articles depuis la liste globale


class Acheteur(Utilisateur):
    def faire_offre(self, article, prix_propose, marge_max=0.1):

    # Utilise proposer_achat() et retourne le résultat

    def rechercher_articles(self, articles, criteres):
# Utilise rechercher() et retourne les résultats
    

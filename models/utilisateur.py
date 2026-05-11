from models import article


class Utilisateur:
    def __init__(self, id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription):
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
        return self.__mot_de_passe

    @mot_de_passe.setter
    def mot_de_passe(self, nouveau_mdp):
        if len(nouveau_mdp) < 6:
            print("Le nouveau mot de passe doit au moins contenir 6 caractères")
            return False
        self.__mot_de_passe = nouveau_mdp
        return True

    def set_mot_de_passe(self, ancien_mdp, nouveau_mdp):
        if ancien_mdp != self.__mot_de_passe:
            print("Ancien mot de passe incorrect")
            return False
        self.mot_de_passe = nouveau_mdp
        return True

    def se_connecter(self, pseudo, mdp):
        if pseudo != self.pseudo:
            print("Pseudo incorrect")
            return False
        if mdp != self.mot_de_passe:
            print("Mot de passe incorrect")
            return False
        print("Vous êtes connectés")
        return True

    def modifier_profil(self, pseudo=None, mail=None, localisation=None):

    # Met à jour les attributs du profil

    def afficher_profil(self):
    # Retourne un résumé de l'utilisateur

class Vendeur(Utilisateur):
    def __init__(self, id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription):
        super().__init__(id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription)
        self.liste_article = []

    def mettre_en_vente(self, article):
        if article.vendu:
            print("L'article est déjà vendu !")
            return False
        self.liste_article.append(article)
        return True

    def retirer_article(self, article):
        if article in self.liste_article:
            self.liste_article.remove(article)
            return True
        else:
            print("Cet article n'existe pas")
            return False
    # Retire un article de la vente

    def mes_articles(self):
        article_vendu = []
        article_en_vente = []
        for a in self.liste_article:
            if a.vendu and a not in article_vendu:
                article_vendu.append(a)
            elif not a.vendu and a not in article_en_vente:
                article_en_vente.append(a)
        return article_vendu, article_en_vente


class Acheteur(Utilisateur):
    def __init__(self, ...):
        super().__init__(...)
        self.favoris = []  # composition — liste d'articles favoris

    def faire_offre(self, article, prix_propose, marge_max=0.1):
        # Utilise proposer_achat() de matching.py
        # Retourne le statut
        ...

    def rechercher_articles(self, articles, criteres):
        # Utilise rechercher() de recherche.py
        # Retourne les résultats
        ...

    def ajouter_favori(self, article):
        # Ajoute un article à self.favoris
        ...

    def retirer_favori(self, article):
        # Retire un article de self.favoris
        ...
    
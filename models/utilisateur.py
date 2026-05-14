""" ----------- Author : LARDILLIER Léo ------------- """
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
            return
        self.__mot_de_passe = nouveau_mdp

    def set_mot_de_passe(self, ancien_mdp, nouveau_mdp):
        if ancien_mdp != self.__mot_de_passe:
            print("Ancien mot de passe incorrect")
            return False
        self.mot_de_passe = nouveau_mdp
        return True
    # Incomplet, manque la persistance BDD

    def se_connecter(self, pseudo, mdp):
        if pseudo != self.pseudo:
            print("Pseudo incorrect")
            return False
        if mdp != self.mot_de_passe:
            print("Mot de passe incorrect")
            return False
        print("Vous êtes connectés")
        return True
    #Incomplet, il faut modifier la DB

    def modifier_profil(self, pseudo=None, mail=None, localisation=None):
        """
        Modifie les informations du profil de l'utilisateur.
        Les paramètres peuvent être None si aucun changement n'est souhaité.
        """
        if pseudo is not None:
            self.pseudo = pseudo
            print(f"Pseudo modifié avec succès : {self.pseudo}")
        if mail is not None:
            self.mail = mail
            print(f"Adresse e-mail modifiée avec succès : {self.mail}")
        if localisation is not None:
            self.localisation = localisation
            print(f"Localisation modifiée avec succès : {self.localisation}")
        if pseudo is None and mail is None and localisation is None:
            print("Aucune modification effectuée.")
            return False
        return True
    #Incomplet, manque la persistance BDD

    def afficher_profil(self):
        return(self.pseudo, self.mail, self.localisation)

class Vendeur(Utilisateur):
    def __init__(self, id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription):
        super().__init__(id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription)
        self.liste_article = []
#persistance BDD OK
    def mettre_en_vente(self, article):
        if article.vendu:
            print("L'article est déjà vendu !")
            return False
        elif article in self.liste_article:
            print("L'article est déjà en vente !")
            return False
        else:
            self.liste_article.append(article)
            from db.db import insert_article
            insert_article(article.nom, article.description, article.categorie, article.sous_categorie, article.genre, article.taille, article.couleur, article.marque, article.etat, article.prix_vendeur, article.prix_min, article.id_vendeur, article.photo, article.matiere)
            return True

    def retirer_article(self, article):
        if article in self.liste_article:
            self.liste_article.remove(article)
            return True
        else:
            print("Cet article n'existe pas")
            return False
    # Retire un article de la vente
    #Incomplet, manque la persistance BDD
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
    def __init__(self, id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription):
        super().__init__(id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription)
        self.favoris = []  # composition — liste d'articles favoris

    def faire_offre(self, article, prix_propose):
        # Utilise proposer_achat() de matching.py
        # Persistance BDD OK
        from services.matching import proposer_achat
        return proposer_achat(self, article, prix_propose)

    def rechercher_articles(self, articles, criteres):
        from services.recherche import scorer_articles
        return scorer_articles(articles, criteres)

    def ajouter_favori(self, article):
        if article not in self.favoris: #Faire un onglet favoris dans la BDD
            self.favoris.append(article)
            return True
        else:
            print("L'article est déjà dans vos favoris !")
            return False
        # Incomplet, manque la persistance BDD

    def retirer_favori(self, article):
        if article in self.favoris: #Faire un onglet favoris dans la BDD
            self.favoris.remove(article)
            return True
        else:
            print("L'article n'est pas dans vos favoris !")
            return False
        # Incomplet, manque la persistance BDD

    
""" ----------- Author : LARDILLIER Léo ------------- """

from typing import Optional, List, Tuple

class Utilisateur:
    """
    Représente un utilisateur inscrit sur la plateforme.
    Classe de base dont héritent Vendeur et Acheteur.
    """

    def __init__(self, id: int, pseudo: str, nom: str, prenom: str, mail: str,
                 mot_de_passe: str, est_pro: bool, evaluation: float,
                 localisation: Optional[str], date_inscription: Optional[str],
                 photo: Optional[str] = None) -> None:
        """
        :param id: identifiant unique de l'utilisateur en base de données
        :param pseudo: nom d'utilisateur public
        :param nom: nom de famille
        :param prenom: prénom
        :param mail: adresse e-mail
        :param mot_de_passe: mot de passe (stocké en attribut privé)
        :param est_pro: True si l'utilisateur est un vendeur professionnel
        :param evaluation: note moyenne attribuée par la communauté (0 à 5)
        :param localisation: ville ou région de l'utilisateur
        :param date_inscription: date d'inscription sur la plateforme
        :param photo: chemin vers la photo de profil
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
        self.photo = photo

    @property
    def mot_de_passe(self) -> str:
        """
        Retourne le mot de passe de l'utilisateur (lecture seule via le setter).

        :return: mot de passe actuel
        """
        return self.__mot_de_passe

    @mot_de_passe.setter
    def mot_de_passe(self, nouveau_mdp: str) -> None:
        """
        Définit un nouveau mot de passe après validation de la longueur minimale.

        :param nouveau_mdp: nouveau mot de passe (doit contenir au moins 6 caractères)
        """
        if len(nouveau_mdp) < 6:
            print("Le nouveau mot de passe doit au moins contenir 6 caractères")
            return
        self.__mot_de_passe = nouveau_mdp

    def set_mot_de_passe(self, ancien_mdp: str, nouveau_mdp: str) -> bool:
        """
        Modifie le mot de passe après vérification de l'ancien mot de passe.

        :param ancien_mdp: mot de passe actuel à vérifier
        :param nouveau_mdp: nouveau mot de passe souhaité (au moins 6 caractères)
        :return: True si le changement a réussi, False sinon
        """
        if ancien_mdp != self.__mot_de_passe:
            print("Ancien mot de passe incorrect")
            return False
        self.mot_de_passe = nouveau_mdp
        from db.db import update_mot_de_passe
        update_mot_de_passe(self.id, self.mot_de_passe)
        return True

    def se_connecter(self, pseudo: str, mdp: str) -> bool:
        """
        Vérifie les identifiants de connexion de l'utilisateur.

        :param pseudo: nom d'utilisateur saisi
        :param mdp: mot de passe saisi
        :return: True si la connexion est réussie, False sinon
        """
        if pseudo != self.pseudo:
            print("Pseudo incorrect")
            return False
        if mdp != self.mot_de_passe:
            print("Mot de passe incorrect")
            return False
        print("Vous êtes connectés")
        return True
    #Incomplet, il faut modifier la DB

    def modifier_profil(self, pseudo: Optional[str] = None,
                        mail: Optional[str] = None,
                        localisation: Optional[str] = None) -> bool:
        """
        Modifie les informations du profil de l'utilisateur.
        Les paramètres non renseignés (None) ne sont pas modifiés.

        :param pseudo: nouveau nom d'utilisateur (optionnel)
        :param mail: nouvelle adresse e-mail (optionnel)
        :param localisation: nouvelle localisation (optionnel)
        :return: True si au moins un champ a été modifié, False sinon
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
        from db.db import update_utilisateur
        update_utilisateur(self.id, pseudo, mail, localisation)
        return True

    def afficher_profil(self) -> Tuple[str, str, Optional[str]]:
        """
        Retourne les informations publiques du profil de l'utilisateur.

        :return: tuple (pseudo, mail, localisation)
        """
        return(self.pseudo, self.mail, self.localisation)


class Vendeur(Utilisateur):
    """
    Représente un utilisateur dans son rôle de vendeur.
    Hérite de Utilisateur et ajoute la gestion des articles mis en vente.
    """

    def __init__(self, id: int, pseudo: str, nom: str, prenom: str, mail: str,
                 mot_de_passe: str, est_pro: bool, evaluation: float,
                 localisation: Optional[str], date_inscription: Optional[str],
                 photo: Optional[str] = None) -> None:
        """
        :param id: identifiant unique de l'utilisateur
        :param pseudo: nom d'utilisateur public
        :param nom: nom de famille
        :param prenom: prénom
        :param mail: adresse e-mail
        :param mot_de_passe: mot de passe
        :param est_pro: True si l'utilisateur est un vendeur professionnel
        :param evaluation: note moyenne attribuée par la communauté (0 à 5)
        :param localisation: ville ou région du vendeur
        :param date_inscription: date d'inscription sur la plateforme
        :param photo: chemin vers la photo de profil
        """
        super().__init__(id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription, photo)
        self.liste_article = self._charger_articles()
        
    def _charger_articles(self):
        """
        Charge les articles du vendeur depuis la base de données.

        :return: liste des articles du vendeur
        """
        from db.db import get_all_articles
        from models.article import Vetement
        articles = []
        for a in get_all_articles():
            if a[7] == self.id:  # id_vendeur est à l'index 7
                articles.append(Vetement(*a))
        return articles

    def mettre_en_vente(self, article: "Article") -> bool:
        """
        Publie un article sur la plateforme et l'enregistre en base de données.

        :param article: instance de Article ou Vetement à mettre en vente
        :return: True si l'article a été ajouté, False s'il est déjà vendu ou déjà en vente
        """
        if article.vendu:
            print("L'article est déjà vendu !")
            return False
        elif any(a.id == article.id for a in self.liste_article):
            print("L'article est déjà en vente !")
            return False
        else:
            self.liste_article.append(article)
            from db.db import insert_article
            article.id = insert_article(article.nom, article.description, article.categorie, article.sous_categorie, article.genre, article.taille, article.couleur, article.marque, article.etat, article.prix_vendeur, article.prix_min, article.id_vendeur, article.photo, article.matiere)
            #Super puissant, car il met à jour la BD avec la fonction insert_article
            #Mais il met directement à jour la plateforme via article.id = 
            return True

    def retirer_article(self, article: "Article") -> bool:
        """
        Retire un article de la liste de vente du vendeur.

        :param article: instance de Article à retirer
        :return: True si l'article a été retiré, False s'il n'était pas en vente
        """
        if article in self.liste_article:
            self.liste_article.remove(article)
            from db.db import delete_article
            delete_article(article.id)
            return True
        else:
            print("Cet article n'existe pas")
            return False

    def mes_articles(self) -> Tuple[List, List]:
        """
        Classe les articles du vendeur en deux catégories : vendus et en vente.

        :return: tuple (liste des articles vendus, liste des articles encore en vente)
        """
        article_vendu = []
        article_en_vente = []
        for a in self.liste_article:
            if a.vendu and a not in article_vendu:
                article_vendu.append(a)
            elif not a.vendu and a not in article_en_vente:
                article_en_vente.append(a)
        return article_vendu, article_en_vente


class Acheteur(Utilisateur):
    """
    Représente un utilisateur dans son rôle d'acheteur.
    Hérite de Utilisateur et ajoute la gestion des favoris et des offres d'achat.
    """

    def __init__(self, id: int, pseudo: str, nom: str, prenom: str, mail: str,
                 mot_de_passe: str, est_pro: bool, evaluation: float,
                 localisation: Optional[str], date_inscription: Optional[str],
                 photo: Optional[str] = None) -> None:
        """
        :param id: identifiant unique de l'utilisateur
        :param pseudo: nom d'utilisateur public
        :param nom: nom de famille
        :param prenom: prénom
        :param mail: adresse e-mail
        :param mot_de_passe: mot de passe
        :param est_pro: True si l'utilisateur est un vendeur professionnel
        :param evaluation: note moyenne attribuée par la communauté (0 à 5)
        :param localisation: ville ou région de l'acheteur
        :param date_inscription: date d'inscription sur la plateforme
        :param photo: chemin vers la photo de profil
        """
        super().__init__(id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription, photo)
        self.favoris = self._charger_favoris()

    def _charger_favoris(self):
        from db.db import get_favoris, get_article_by_id
        from models.article import Vetement
        favoris = []
        for favori in get_favoris(self.id):
            id_objet = favori[2]
            article = get_article_by_id(id_objet)
            if article:
                favoris.append(Vetement(*article))
        return favoris

    def faire_offre(self, article: "Article", prix_propose: float) -> str:
        """
        Soumet une offre d'achat sur un article et déclenche l'algorithme de négociation.

        :param article: instance de Article sur lequel faire une offre
        :param prix_propose: prix proposé par l'acheteur (en euros)
        :return: statut de la transaction ('acceptee', 'negociation' ou 'refusee')
        """
        from services.matching import proposer_achat
        return proposer_achat(self, article, prix_propose)

    def rechercher_articles(self, articles: List, criteres: dict) -> List[Tuple]:
        """
        Recherche et classe des articles selon des critères de filtrage.

        :param articles: liste de tous les articles disponibles
        :param criteres: dictionnaire de critères (ex. {'taille': 'M', 'couleur': 'Bleu'})
        :return: liste de tuples (article, score) triés par pertinence décroissante
        """
        from services.recherche import scorer_articles
        return scorer_articles(articles, criteres)

    def ajouter_favori(self, article: "Article") -> bool:
        """
        Ajoute un article à la liste des favoris de l'acheteur.

        :param article: instance de Article à ajouter aux favoris
        :return: True si l'ajout a réussi, False si l'article est déjà en favori
        """
        if article not in self.favoris:
            self.favoris.append(article)
            from db.db import insert_favori
            insert_favori(self.id, article.id)
            return True
        else:
            print("L'article est déjà dans vos favoris !")
            return False

    def retirer_favori(self, article: "Article") -> bool:
        """
        Retire un article de la liste des favoris de l'acheteur.

        :param article: instance de Article à retirer des favoris
        :return: True si le retrait a réussi, False si l'article n'était pas en favori
        """
        if article in self.favoris:
            self.favoris.remove(article)
            from db.db import delete_favori
            delete_favori(self.id, article.id)
            return True
        else:
            print("L'article n'est pas dans vos favoris !")
            return False

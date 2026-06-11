""" ----------- Author : LARDILLIER Léo ------------- """

from typing import Optional
from services.observer import Observable, Observateur
class Plateforme(Observable):
    """
    Contrôleur central de la marketplace ENSTADUSTYLE.
    Gère les utilisateurs, le catalogue d'articles et les transactions.
    Sert de point d'entrée pour toutes les opérations de la plateforme.
    """

    def __init__(self) -> None:
        """
        Initialise une plateforme vide avec des listes d'utilisateurs, d'articles et de transactions.
        """
        super().__init__()        # Initialise self.observateur par composition
        self.utilisateurs = []    # composition
        self.articles = []        # composition
        self.transactions = []    # composition
        self.utilisateur_courant = None #Authentification
        self.notifications = []

    def charger_depuis_bdd(self) -> bool:
        """
        Charge l'ensemble des utilisateurs et des articles depuis la base de données SQLite.
        Peuple les listes self.utilisateurs et self.articles en mémoire.

        :return: True une fois le chargement effectué
        """
        self.utilisateur_courant = "admin" #Permet de passer l'authent
        from db.db import get_all_utilisateurs, get_all_articles, get_all_abonnements_notif, migrer_photo_utilisateur
        migrer_photo_utilisateur()
        from models.utilisateur import Utilisateur
        from models.article import Vetement
        utilisateurs_bdd = get_all_utilisateurs()
        self.utilisateurs = [Utilisateur(*u) for u in utilisateurs_bdd]
        articles_bdd = get_all_articles()
        self.articles = [Vetement(*a) for a in articles_bdd]
        #manque un get_all_transactions ??
        for obs in get_all_abonnements_notif():
            id_user = obs[1]
            criteres = obs[2]
            user = self.trouver_utilisateur_id(id_user)
            if user:
                acheteur = self.en_tant_que_acheteur(user)
                observateur = Observateur(acheteur, criteres, plateforme=self)
                self._observateurs.append(observateur)
        self.utilisateur_courant = None
        return True


    def authentifier_utilisateur(self, log, password):
        """
        Vérifie les identifiants et connecte l'utilisateur si valides.

        :param log: pseudo saisi par l'utilisateur
        :param password: mot de passe saisi
        :return: instance Utilisateur connecté, ou None si identifiants incorrects
        """
        for user in self.utilisateurs:
            if log == user.pseudo:
                if password == user.mot_de_passe:
                    self.utilisateur_courant = user
                    print("Vous êtes connecté en tant que " + user.pseudo + ".")
                    return(self.trouver_utilisateur(log))
        self.utilisateur_courant = None
        print('Identifiants incorrects.')
        return None

    def need_auth(func):
        """Décorateur : bloque l'appel si aucun utilisateur n'est connecté."""
        def wrapper(self, *args, **kwargs):
            if self.utilisateur_courant is None:
                print("Vous devez être connecté !")
                return False
            return func(self, *args, **kwargs)
        return wrapper

    @need_auth
    def deconnecter_utilisateur(self):
        """Déconnecte l'utilisateur courant et réinitialise la session."""
        self.utilisateur_courant = None
        return("Vous êtes déconnecté.")


    def creer_utilisateur(self, pseudo: str, nom: str, prenom: str, mail: str,
                          mot_de_passe: str, est_pro: bool = False, evaluation: float = 0,
                          localisation: Optional[str] = None,
                          date_inscription: Optional[str] = None) -> bool:
        """
        Crée un nouvel utilisateur, vérifie l'unicité du pseudo et l'enregistre en base de données.

        :param pseudo: nom d'utilisateur unique
        :param nom: nom de famille
        :param prenom: prénom
        :param mail: adresse e-mail
        :param mot_de_passe: mot de passe (non hashé)
        :param est_pro: True si l'utilisateur est un vendeur professionnel (défaut : False)
        :param evaluation: note de départ attribuée (défaut : 0)
        :param localisation: ville ou région de l'utilisateur (optionnel)
        :param date_inscription: date d'inscription (optionnel, None par défaut)
        :return: True si l'utilisateur a été créé, False si le pseudo est déjà utilisé
        """
        for user in self.utilisateurs:
            if pseudo == user.pseudo:
                print('Pseudonyme déjà utilisé, veuillez en choisir un autre.')
                return False
        from models.utilisateur import Utilisateur
        from db.db import insert_utilisateur
        #Créer la variable new_id met à jour la BDD
        new_id = insert_utilisateur(pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation)
        new_user = Utilisateur(new_id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation,
                 date_inscription)
        self.utilisateurs.append(new_user)
        return True

    def trouver_utilisateur(self, pseudo: str) -> Optional["Utilisateur"]:
        """
        Recherche un utilisateur par son pseudo dans la liste en mémoire.

        :param pseudo: nom d'utilisateur à rechercher
        :return: instance de Utilisateur si trouvé, None sinon
        """
        for user in self.utilisateurs:
            if pseudo == user.pseudo:
                return user
        return None

    def trouver_utilisateur_id(self, id):
        """
        Recherche un utilisateur par son identifiant numérique.

        :param id: identifiant unique de l'utilisateur
        :return: instance Utilisateur si trouvé, None sinon
        """
        for user in self.utilisateurs:
            if id == user.id:
                return user
        return None

    @need_auth
    def ajouter_article(self, article: "Article") -> bool:
        """
        Ajoute un article au catalogue de la plateforme s'il n'y est pas déjà.

        :param article: instance de Article ou Vetement à ajouter
        :return: True si l'article a été ajouté, False s'il était déjà présent
        """
        if article not in self.articles:
            self.articles.append(article)
            self.notifier(article)
            return True
        return False

    def afficher_catalogue(self) -> None:
        """
        Affiche dans la console tous les articles du catalogue avec leur prix et statut de vente.
        """
        for a in self.articles:
            if not a.vendu:
                print(f"{a.nom} — {a.prix_vendeur}€ ({a.sous_categorie})")
            else:
                print(f"{a.nom} — {a.prix_vendeur}€ ({a.sous_categorie}) — Vendu")

    def en_tant_que_acheteur(self, utilisateur: "Utilisateur") -> "Acheteur":
        """
        Convertit un Utilisateur en instance Acheteur pour accéder aux fonctionnalités d'achat.
        Tous les utilisateurs sont chargés comme Utilisateur de base, puis convertis au besoin.

        :param utilisateur: instance de Utilisateur à convertir
        :return: instance de Acheteur avec les mêmes données que l'utilisateur
        """
        from models.utilisateur import Acheteur
        return Acheteur(utilisateur.id, utilisateur.pseudo, utilisateur.nom,
                        utilisateur.prenom, utilisateur.mail, utilisateur.mot_de_passe,
                        utilisateur.est_pro, utilisateur.evaluation,
                        utilisateur.localisation, utilisateur.date_inscription,
                        getattr(utilisateur, 'photo', None))

    @need_auth
    def en_tant_que_vendeur(self, utilisateur: "Utilisateur") -> "Vendeur":
        """
        Convertit un Utilisateur en instance Vendeur et charge ses articles existants.
        Tous les utilisateurs sont chargés comme Utilisateur de base, puis convertis au besoin.

        :param utilisateur: instance de Utilisateur à convertir
        :return: instance de Vendeur avec les mêmes données que l'utilisateur et ses articles chargés
        """
        from models.utilisateur import Vendeur
        vendeur = Vendeur(utilisateur.id, utilisateur.pseudo, utilisateur.nom,
                          utilisateur.prenom, utilisateur.mail, utilisateur.mot_de_passe,
                          utilisateur.est_pro, utilisateur.evaluation,
                          utilisateur.localisation, utilisateur.date_inscription,
                          getattr(utilisateur, 'photo', None))
        return vendeur

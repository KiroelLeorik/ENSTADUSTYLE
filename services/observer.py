""" ----------- Author : LARDILLIER Léo / GREGOIRE Louna ------------- """

from models.utilisateur import Acheteur
from services.recherche import rechercher

class Observateur:
    """
    Représente un abonné aux notifications d'articles.
    Vérifie si un nouvel article correspond aux critères de l'acheteur et le notifie si oui.
    """

    def __init__(self, acheteur, criteres, plateforme=None):
        """
        :param acheteur: instance Acheteur abonné à la notification
        :param criteres: dict de filtres (ex. {'taille': 'M', 'couleur': 'Bleu'})
        :param plateforme: instance Plateforme pour stocker la notification (optionnel)
        """
        self.acheteur = acheteur
        self.criteres = criteres
        self.plateforme = plateforme

    def update(self, article):
        """
        Appelé par Observable.notifier() à chaque nouvel article publié.
        Vérifie si l'article correspond aux critères et stocke la notification.

        :param article: instance Article nouvellement mis en vente
        """
        resultat = rechercher([article], self.criteres)
        if resultat:
            print(f"[NOTIFICATION] {self.acheteur.pseudo} : "
                  f"'{article.nom}' correspond à vos critères !")
            if self.plateforme:
                self.plateforme.notifications.append(article)


class Observable:
    """
    Sujet du pattern Observer — implémenté par Plateforme.
    Gère la liste des observateurs et les notifie lors d'un nouvel article.
    """

    def __init__(self):
        """Initialise la liste des observateurs actifs."""
        self._observateurs = []

    def abonner(self, observateur):
        """
        Enregistre un observateur et persiste l'abonnement en base de données.

        :param observateur: instance Observateur à ajouter
        :return: True si ajouté, False si déjà présent
        """
        if observateur not in self._observateurs:
            from db.db import insert_abonnement_notif
            self._observateurs.append(observateur)
            insert_abonnement_notif(observateur.acheteur.id, observateur.criteres)
            return True
        return False

    def desabonner(self, observateur):
        """
        Supprime un observateur et retire l'abonnement de la base de données.

        :param observateur: instance Observateur à retirer
        :return: True si retiré, False s'il n'était pas abonné
        """
        if observateur in self._observateurs:
            from db.db import delete_abonnement_notif
            self._observateurs.remove(observateur)
            delete_abonnement_notif(observateur.acheteur.id, observateur.criteres)
            return True
        return False

    def notifier(self, article):
        """
        Notifie tous les observateurs enregistrés d'un nouvel article publié.

        :param article: instance Article nouvellement mis en vente
        """
        for observateur in self._observateurs:
            observateur.update(article)





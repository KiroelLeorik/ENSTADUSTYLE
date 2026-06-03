from models.utilisateur import Acheteur
from services.recherche import rechercher

class Observateur:
    """Interface que chaque acheteur devra implémenter"""
    def __init__(self, acheteur, criteres, plateforme=None):
        self.acheteur = acheteur
        self.criteres = criteres
        self.plateforme = plateforme
    def update(self, article):
        resultat = rechercher([article], self.criteres)
        if resultat:
            # Pour l'instant : print
            # Plus tard : signal PyQt5, popup, badge...
            print(f"[NOTIFICATION] {self.acheteur.pseudo} : "
                  f"'{article.nom}' correspond à vos critères !")
            if self.plateforme:
                self.plateforme.notifications.append(article)
            #On peut imaginer qu'on envoi un mail aussi !

class Observable:
    """Le sujet — ici ce sera la Plateforme"""

    def __init__(self):
        self._observateurs = []

    def abonner(self, observateur): #Observateur est un objet de type Observateur
        if observateur not in self._observateurs:
            from db.db import insert_abonnement_notif
            self._observateurs.append(observateur)
            insert_abonnement_notif(observateur.acheteur.id, observateur.criteres)
            return True
        return False

    def desabonner(self, observateur):
        if observateur in self._observateurs:
            from db.db import delete_abonnement_notif
            self._observateurs.remove(observateur)
            delete_abonnement_notif(observateur.acheteur.id, observateur.criteres)
            return True
        return False

    def notifier(self, article):
        for observateur in self._observateurs:
            observateur.update(article)





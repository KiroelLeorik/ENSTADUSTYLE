from models.utilisateur import Acheteur
from services.recherche import rechercher


class Observable:
    """Le sujet — ici ce sera la Plateforme"""

    def __init__(self):
        self._observateurs = []

    def abonner(self, observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)
            return True
        return False

    def desabonner(self, observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)
            return True
        return False

    def notifier(self, article):
        for observateur in self._observateurs:
            observateur.update(article)



class Observateur:
    """Interface que chaque acheteur devra implémenter"""
    def __init__(self, acheteur, criteres):
        self.acheteur = acheteur
        self.criteres = criteres

    def update(self, article):
        resultat = rechercher([article], self.criteres)
        if resultat:
            # Pour l'instant : print
            # Plus tard : signal PyQt5, popup, badge...
            print(f"[NOTIFICATION] {self.acheteur.pseudo} : "
                  f"'{article.nom}' correspond à vos critères !")
            #On peut imaginer qu'on envoi un mail aussi !

class Utilisateur:
    def __init__(self, id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription):
        self.id = id
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.mot_de_passe = mot_de_passe
        self.est_pro = est_pro
        self.evaluation = evaluation
        self.localisation = localisation
        self.date_inscription = date_inscription
    def se_connecter(self):
        print("Vous êtes connectés")

class Vendeur(Utilisateur):
    pass


class Acheteur(Utilisateur):
    pass
    
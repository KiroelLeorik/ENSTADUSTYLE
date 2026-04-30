class Utilisateur:
    def __init__(self, pseudo, mail, localisation, evaluation, est_pro:
        self.pseudo = pseudo
        self.mail = mail
        self.localisation = localisation
        self.evaluation = evaluation
        self.est_pro = est_pro

    def se_connecter(self):
        print("Vous êtes connectés")

class Vendeur(Utilisateur):
    pass


class Acheteur(Utilisateur):
    pass
    
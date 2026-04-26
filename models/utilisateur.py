class utilisateur(pseudo, mail, localisation, mail):
    def __init__(self, pseudo, mail, localisation, evaluation):
        self.pseudo = pseudo
        self.mail = mail
        self.localisation = localisation
        self.evaluation = evaluation
    def se_connecter(self):
        print("Vous êtes connectés")

class vendeur(utilisateur):
    def __init__(self, pseudo, mail, localisation, evaluation):
        super().__init__(pseudo, mail, localisation, evaluation)

class acheteur(utilisateur):
    def __init__(self, pseudo, mail, localisation, evaluation):
        super().__init__(pseudo, mail, localisation, evaluation)
    
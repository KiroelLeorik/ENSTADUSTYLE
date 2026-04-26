class Objet(nom, description, prix_vendeur, prix_min, etat):
    def __init__(self, nom, description, prix_vendeur, prix_min, etat):
        self.nom = nom
        self.description = description
        self.prix_vendeur = prix_vendeur
        self.prix_min = prix_min
        self.etat = etat
    def est_disponible(self):
        return self.etat == True

class vetement(objet):
    def __init__(self, nom, description, prix_vendeur, prix_min, etat, taille, couleur, marque, genre):
        super().__init__(nom, description, prix_vendeur, prix_min, etat)
        self.taille = taille
        self.couleur = couleur
        self.marque = marque
        self.genre = genre

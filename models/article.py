class Article:
    def __init__(self, nom, description, prix_vendeur, prix_min, etat):
        self.nom = nom
        self.description = description
        self.prix_vendeur = prix_vendeur
        self.prix_min = prix_min
        self.etat = etat
        self.vendu = False  # par défaut un article est disponible

    def est_disponible(self):
        return not self.vendu

class Vetement(Article):
    def __init__(self, nom, description, prix_vendeur, prix_min, etat, taille, couleur, marque, genre):
        super().__init__(nom, description, prix_vendeur, prix_min, etat)
        self.taille = taille
        self.couleur = couleur
        self.marque = marque
        self.genre = genre


if __name__ == "__main__":

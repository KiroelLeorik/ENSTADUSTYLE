class Article:
    def __init__(self, id, nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, date_publication, photo, matiere, vendu):
        """

        :param id:
        :param nom:
        :param description:
        :param categorie:
        :param sous_categorie:
        :param genre:
        :param taille:
        :param couleur:
        :param marque:
        :param etat:
        :param prix_vendeur:
        :param prix_min:
        :param id_vendeur:
        :param date_publication:
        :param photo:
        :param matiere:
        """
        self.id = id
        self.nom = nom
        self.description = description
        self.categorie = categorie
        self.sous_categorie = sous_categorie
        self.genre = genre
        self.taille = taille
        self.couleur = couleur
        self.marque = marque
        self.etat = etat
        self.prix_vendeur = prix_vendeur
        self.prix_min = prix_min
        self.id_vendeur = id_vendeur
        self.date_publication = date_publication
        self.photo = photo
        self.vendu = vendu
        self.matiere = matiere
    def est_disponible(self):
        """
    
        :param self:
        :return:
        """
        return not self.vendu

class Vetement(Article):
    def __init__(self, id, nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, date_publication, photo, matiere, vendu):
        """

        :param id:
        :param nom:
        :param description:
        :param categorie:
        :param sous_categorie:
        :param genre:
        :param taille:
        :param couleur:
        :param marque:
        :param etat:
        :param prix_vendeur:
        :param prix_min:
        :param id_vendeur:
        :param date_publication:
        :param photo:
        :param matiere:
        """
        super().__init__(id, nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, date_publication, photo, matiere, vendu)
        def get_details(self):
            """

            :param self:
            :return:
            """
            return [self.marque, self.taille, self.couleur, self.matiere]


if __name__ == "__main__":
    pass

""" ----------- Author : LARDILLIER Léo ------------- """

class Article:
    """
    Classe représentant un article de la base de donnée.
    """
    def __init__(self, id, nom, description, categorie, prix_vendeur,
                 prix_min, etat, id_vendeur, date_publication, photo, vendu=0):
        """
        :param id: identifiant unique de l'article
        :param nom: nom donnée à l'article par le vendeur
        :param description: descrption donnée à l'article par le vendeur
        :param categorie: catégorie à laquelle l'article appartient
        :param prix_vendeur: prix fixé par le vendeur
        :param prix_min: prix minimum acceptable par le vendeur
        :param etat: état de dégradation de l'article
        :param id_vendeur: identifiant unique du vendeur
        :param date_publication: date de publication de l'article
        :param photo: chemin vers un fichier PNG
        :param vendu: True ou False, indique si l'article est vendu
        """
        self.id = id
        self.nom = nom
        self.description = description
        self.categorie = categorie
        self.prix_vendeur = prix_vendeur
        self.prix_min = prix_min
        self.etat = etat
        self.id_vendeur = id_vendeur
        self.date_publication = date_publication
        self.photo = photo
        self.vendu = bool(vendu)

    def est_disponible(self):
        """
        Vérifie si l'article est disponible pour la vente.
        :return: True si l'article n'est pas vendu, False sinon.
        """
        return not self.vendu

class Vetement(Article):
    """
    Représente un bêtement mis en vente sur la plateforme.
    Hérite de Article et ajoute les cartactéristiques propres aux vêtements
    """
    def __init__(self, id, nom, description, categorie, prix_vendeur,
                 prix_min, etat, id_vendeur, date_publication, photo, vendu=0,
                 sous_categorie=None, genre=None, taille=None, couleur=None,
                 marque=None, matiere=None):
        """
        :param sous_categorie: sous_categorie (Veste, Jean, ...)
        :param genre: catégorie de genre ciblée par le vêtement
        :param taille: taille (XS, S, M, L, XL, XXL)
        :param couleur: couleur du vêtement (noir, blanc, rouge, ...)
        :param marque: marque du vêtement (Zara, H&M, ...)
        :param matiere: matière du vêtement (Coton, Jean, ...)
        """
        super().__init__(id, nom, description, categorie, prix_vendeur,
                        prix_min, etat, id_vendeur, date_publication, photo, vendu)
        self.sous_categorie = sous_categorie
        self.genre = genre
        self.taille = taille
        self.couleur = couleur
        self.marque = marque
        self.matiere = matiere

    def get_details(self):
        """
        :return: Renvoi les informations basiques à propos du vêtement
        """
        return f"{self.marque} - {self.taille} - {self.couleur} - {self.matiere}"
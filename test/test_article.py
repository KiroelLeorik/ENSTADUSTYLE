""" ----------- Author : LARDILLIER Léo ------------- """

import unittest
from models.article import Article, Vetement


class TestArticle(unittest.TestCase):

    def setUp(self):
        """
        
        :param self: 
        :return: 
        """
        """Crée un article et un vêtement de test réutilisables avant chaque test"""
        self.article = Article(
            id=1, nom="Veste en jean", description="Très belle veste",
            categorie="Vêtements", etat="bon",
            prix_vendeur=35.0, prix_min=25.0, id_vendeur=1,
            date_publication="2026-04-10", photo="veste.jpg"
        )
        self.vetement = Vetement(
            id=2, nom="Robe fleurie", description="Robe d'été légère",
            categorie="Vêtements", sous_categorie="Robes", genre="Femme",
            taille="S", couleur="Multicolore", marque="Zara", etat="tres_bon",
            prix_vendeur=20.0, prix_min=15.0, id_vendeur=2,
            date_publication="2026-04-12", photo="robe.jpg", matiere="Coton"
        )
    # --- Test 1 : Création d'un article ---
    def test_creation_nom(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que le nom est bien assigné"""
        self.assertEqual(self.article.nom, "Veste en jean")

    def test_creation_prix(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que le prix vendeur est bien assigné"""
        self.assertEqual(self.article.prix_vendeur, 35.0)

    # --- Test 2 : Disponibilité ---
    def test_disponible_par_defaut(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie qu'un article est disponible par défaut"""
        self.assertTrue(self.article.est_disponible())

    def test_non_disponible_si_vendu(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie qu'un article vendu n'est plus disponible"""
        self.article.vendu = True
        self.assertFalse(self.article.est_disponible())

    # --- Test 3 : Prix minimum ---
    def test_prix_min_inferieur_prix_vendeur(self):
        """
        Vérifie que le prix minimum est inférieur au prix vendeur
        :param self: 
        :return: 
        """

        self.assertLess(self.article.prix_min, self.article.prix_vendeur)

    def test_prix_min_valeur(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que le prix minimum correspond à la valeur donnée"""
        self.assertEqual(self.article.prix_min, 25.0)

    # --- Test 4 : Héritage Vetement ---
    def test_vetement_est_article(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que Vetement hérite bien de Article"""
        self.assertIsInstance(self.vetement, Article)

    def test_vetement_get_details(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que get_details retourne bien une chaîne de caractères"""
        details = self.vetement.get_details()
        self.assertIsInstance(details, str)


if __name__ == '__main__':
    unittest.main()


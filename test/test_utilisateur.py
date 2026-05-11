import unittest
from models.utilisateur import Utilisateur, Vendeur, Acheteur


class TestUtilisateur(unittest.TestCase):

    def setUp(self):
            """
    
    :param self: 
    :return: 
    """
        """Crée un utilisateur de test réutilisable avant chaque test"""
        self.user = Utilisateur(
            id=1, pseudo="alice92", nom="Martin", prenom="Alice",
            mail="alice@mail.com", mot_de_passe="motdepasse",
            est_pro=0, evaluation=4.8, localisation="Paris",
            date_inscription="2026-01-01"
        )
        self.vendeur = Vendeur(
            id=2, pseudo="bob_style", nom="Durand", prenom="Bob",
            mail="bob@mail.com", mot_de_passe="motdepasse",
            est_pro=0, evaluation=4.5, localisation="Lyon",
            date_inscription="2026-01-01"
        )
        self.acheteur = Acheteur(
            id=3, pseudo="sophie_mode", nom="Leroy", prenom="Sophie",
            mail="sophie@mail.com", mot_de_passe="motdepasse",
            est_pro=0, evaluation=4.9, localisation="Marseille",
            date_inscription="2026-01-01"
        )

    # --- Test 1 : Création d'un utilisateur ---
    def test_creation_pseudo(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que le pseudo est bien assigné"""
        self.assertEqual(self.user.pseudo, "alice92")

    def test_creation_localisation(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que la localisation est bien assignée"""
        self.assertEqual(self.user.localisation, "Paris")

    # --- Test 2 : Evaluation ---
    def test_evaluation_valide(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que l'évaluation est bien un nombre entre 0 et 5"""
        self.assertGreaterEqual(self.user.evaluation, 0)
        self.assertLessEqual(self.user.evaluation, 5)

    def test_evaluation_valeur(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que l'évaluation correspond à la valeur donnée"""
        self.assertEqual(self.user.evaluation, 4.8)

    # --- Test 3 : Héritage Vendeur ---
    def test_vendeur_est_utilisateur(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que Vendeur hérite bien de Utilisateur"""
        self.assertIsInstance(self.vendeur, Utilisateur)

    def test_vendeur_a_pseudo(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que Vendeur a bien accès aux attributs de Utilisateur"""
        self.assertEqual(self.vendeur.pseudo, "bob_style")

    # --- Test 4 : Héritage Acheteur ---
    def test_acheteur_est_utilisateur(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que Acheteur hérite bien de Utilisateur"""
        self.assertIsInstance(self.acheteur, Utilisateur)

    def test_acheteur_a_localisation(self):
        """
        
        :param self: 
        :return: 
        """
        """Vérifie que Acheteur a bien accès aux attributs de Utilisateur"""
        self.assertEqual(self.acheteur.localisation, "Marseille")


if __name__ == '__main__':
    unittest.main()

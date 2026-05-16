import unittest
from models.utilisateur import Utilisateur, Vendeur, Acheteur
from models.article import Article, Vetement
from models.transaction import Transaction
from models.plateforme import Plateforme
from services.matching import proposer_achat
from services.recherche import rechercher


class TestTransaction(unittest.TestCase):
    """
    Tests unitaires pour la classe Transaction.
    Author : Lardillier Léo
    """

    def setUp(self):
        """Initialise les objets de test avant chaque test."""
        self.acheteur = Utilisateur(1, "alice92", "Martin", "Alice", "alice@mail.com",
                                    "hash1", 0, 4.8, "Paris", "2026-01-01")
        self.article = Vetement(1, "Veste en jean", "Belle veste", "Vêtements",
                                35.0, 25.0, "bon", 2, "2026-04-10", "veste.jpg", 0,
                                "Vestes", "Femme", "M", "Bleu", "Levi's", "Denim")
        self.transaction = Transaction(self.acheteur, None, self.article, 30.0, None, "negociation")

    def test_creation_statut(self):
        """Vérifie que le statut est bien assigné à la création."""
        self.assertEqual(self.transaction.statut, "negociation")

    def test_creation_prix_propose(self):
        """Vérifie que le prix proposé est bien enregistré."""
        self.assertEqual(self.transaction.prix_propose, 30.0)

    def test_creation_acheteur(self):
        """Vérifie que l'acheteur est bien associé à la transaction."""
        self.assertEqual(self.transaction.acheteur.pseudo, "alice92")

    def test_creation_article(self):
        """Vérifie que l'article est bien associé à la transaction."""
        self.assertEqual(self.transaction.article.nom, "Veste en jean")


class TestPlateforme(unittest.TestCase):
    """
    Tests unitaires pour la classe Plateforme.
    Auteur : [Prenom NOM - Personne A]
    """

    def setUp(self):
        """Initialise une plateforme et des objets de test."""
        self.p = Plateforme()
        self.article = Vetement(1, "Veste en jean", "Belle veste", "Vêtements",
                                35.0, 25.0, "bon", 1, "2026-04-10", "veste.jpg", 0,
                                "Vestes", "Femme", "M", "Bleu", "Levi's", "Denim")

    def test_ajouter_article(self):
        """Vérifie qu'un article est bien ajouté au catalogue."""
        self.p.ajouter_article(self.article)
        self.assertIn(self.article, self.p.articles)

    def test_ajouter_article_doublon(self):
        """Vérifie qu'un article en double n'est pas ajouté."""
        self.p.ajouter_article(self.article)
        self.p.ajouter_article(self.article)
        self.assertEqual(len(self.p.articles), 1)

    def test_trouver_utilisateur_existant(self):
        """Vérifie qu'un utilisateur existant est bien trouvé."""
        user = Utilisateur(1, "alice92", "Martin", "Alice", "alice@mail.com",
                          "hash1", 0, 4.8, "Paris", "2026-01-01")
        self.p.utilisateurs.append(user)
        result = self.p.trouver_utilisateur("alice92")
        self.assertEqual(result.pseudo, "alice92")

    def test_trouver_utilisateur_inexistant(self):
        """Vérifie que None est retourné si l'utilisateur n'existe pas."""
        result = self.p.trouver_utilisateur("pseudo_inexistant")
        self.assertIsNone(result)


class TestMatching(unittest.TestCase):
    """
    Tests unitaires pour l'algorithme de matching acheteur/vendeur.
    Auteur : [Prenom NOM - Personne B]
    """

    def setUp(self):
        """Initialise un acheteur et un article de test."""
        self.acheteur = Utilisateur(1, "alice92", "Martin", "Alice", "alice@mail.com",
                                    "hash1", 0, 4.8, "Paris", "2026-01-01")
        self.article = Vetement(1, "Veste en jean", "Belle veste", "Vêtements",
                                35.0, 25.0, "bon", 2, "2026-04-10", "veste.jpg", 0,
                                "Vestes", "Femme", "M", "Bleu", "Levi's", "Denim")

    def test_achat_accepte(self):
        """Vérifie qu'une offre >= prix_vendeur est acceptée."""
        statut = proposer_achat(self.acheteur, self.article, 40.0)
        self.assertEqual(statut, "acceptee")

    def test_achat_accepte_exact(self):
        """Vérifie qu'une offre exactement au prix_vendeur est acceptée."""
        statut = proposer_achat(self.acheteur, self.article, 35.0)
        self.assertEqual(statut, "acceptee")

    def test_negociation(self):
        """Vérifie qu'une offre entre prix_min et prix_vendeur déclenche une négociation."""
        statut = proposer_achat(self.acheteur, self.article, 30.0)
        self.assertEqual(statut, "negociation")

    def test_negociation_prix_min_exact(self):
        """Vérifie qu'une offre exactement au prix_min déclenche une négociation."""
        statut = proposer_achat(self.acheteur, self.article, 25.0)
        self.assertEqual(statut, "negociation")

    def test_achat_refuse(self):
        """Vérifie qu'une offre < prix_min est refusée."""
        statut = proposer_achat(self.acheteur, self.article, 20.0)
        self.assertEqual(statut, "refusee")

    def test_achat_refuse_zero(self):
        """Vérifie qu'une offre à 0€ est refusée."""
        statut = proposer_achat(self.acheteur, self.article, 0.0)
        self.assertEqual(statut, "refusee")


class TestRecherche(unittest.TestCase):
    """
    Tests unitaires pour l'algorithme de recherche.
    Auteur : [Prenom NOM - Personne B]
    """

    def setUp(self):
        """Initialise une liste d'articles de test."""
        self.articles = [
            Vetement(1, "Veste en jean", "Belle veste", "Vêtements", 35.0, 25.0,
                     "bon", 1, "2026-04-10", "veste.jpg", 0,
                     "Vestes", "Femme", "M", "Bleu", "Levi's", "Denim"),
            Vetement(2, "Robe fleurie", "Robe légère", "Vêtements", 20.0, 15.0,
                     "tres_bon", 2, "2026-04-12", "robe.jpg", 0,
                     "Robes", "Femme", "S", "Multicolore", "Zara", "Coton"),
            Vetement(3, "Hoodie Nike", "Hoodie gris", "Vêtements", 40.0, 28.0,
                     "neuf", 3, "2026-04-15", "hoodie.jpg", 0,
                     "Sweats", "Homme", "XL", "Gris", "Nike", "Coton"),
        ]

    def test_recherche_sous_categorie(self):
        """Vérifie que le filtre par sous_categorie retourne les bons articles."""
        resultats = rechercher(self.articles, {"sous_categorie": "Vestes"})
        self.assertEqual(len(resultats), 1)
        self.assertEqual(resultats[0].nom, "Veste en jean")

    def test_recherche_plusieurs_criteres(self):
        """Vérifie que la recherche multi-critères fonctionne."""
        resultats = rechercher(self.articles, {"couleur": "Gris", "marque": "Nike"})
        self.assertEqual(len(resultats), 1)
        self.assertEqual(resultats[0].nom, "Hoodie Nike")

    def test_recherche_criteres_vides(self):
        """Vérifie que des critères vides retournent tous les articles disponibles."""
        resultats = rechercher(self.articles, {})
        self.assertEqual(len(resultats), 3)

    def test_recherche_article_vendu_exclu(self):
        """Vérifie qu'un article vendu n'apparaît pas dans les résultats."""
        self.articles[0].vendu = True
        resultats = rechercher(self.articles, {})
        self.assertEqual(len(resultats), 2)


if __name__ == '__main__':
    unittest.main()

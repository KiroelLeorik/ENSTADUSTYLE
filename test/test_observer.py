"""Tests unitaires pour le pattern Observer — Author : LARDILLIER Léo"""

import unittest
from unittest.mock import patch, MagicMock
from models.article import Vetement
from models.utilisateur import Utilisateur
from services.observer import Observateur, Observable


def _make_article(id=1, nom="Veste bleue", vendu=0, taille="M", couleur="Bleu",
                  sous_categorie="Vestes"):
    return Vetement(id, nom, "desc", "Vêtements", 30.0, 20.0, "bon", 2,
                    "2026-01-01", None, vendu,
                    sous_categorie, "Femme", taille, couleur, "Zara", "Coton")


def _make_acheteur(id=1, pseudo="alice92"):
    return Utilisateur(id, pseudo, "Martin", "Alice", "a@mail.com",
                       "pwd", 0, 4.5, "Paris", "2026-01-01")


class TestObservateur(unittest.TestCase):

    def setUp(self):
        self.acheteur = _make_acheteur()
        self.plateforme = MagicMock()
        self.plateforme.notifications = []

    def test_update_article_correspondant(self):
        """Un article correspondant aux critères génère une notification."""
        obs = Observateur(self.acheteur, {"taille": "M", "couleur": "Bleu"}, self.plateforme)
        article = _make_article(taille="M", couleur="Bleu")
        obs.update(article)
        self.assertIn(article, self.plateforme.notifications)

    def test_update_article_non_correspondant(self):
        """Un article ne correspondant pas aux critères ne génère pas de notification."""
        obs = Observateur(self.acheteur, {"taille": "M", "couleur": "Bleu"}, self.plateforme)
        article = _make_article(taille="XL", couleur="Rouge")
        obs.update(article)
        self.assertNotIn(article, self.plateforme.notifications)

    def test_update_correspondance_partielle(self):
        """Correspondance partielle (1 critère sur 2) ne déclenche pas de notification."""
        obs = Observateur(self.acheteur, {"taille": "M", "couleur": "Bleu"}, self.plateforme)
        article = _make_article(taille="M", couleur="Rouge")
        obs.update(article)
        self.assertNotIn(article, self.plateforme.notifications)

    def test_update_sans_plateforme(self):
        """update() sans plateforme ne lève pas d'erreur."""
        obs = Observateur(self.acheteur, {"taille": "M"})
        article = _make_article(taille="M")
        try:
            obs.update(article)
        except Exception as e:
            self.fail(f"update() a levé une exception inattendue : {e}")

    def test_criteres_vides(self):
        """Critères vides → tous les articles correspondent."""
        obs = Observateur(self.acheteur, {}, self.plateforme)
        article = _make_article()
        obs.update(article)
        self.assertIn(article, self.plateforme.notifications)


class TestObservable(unittest.TestCase):

    def setUp(self):
        self.observable = Observable()
        self.acheteur = _make_acheteur()

    @patch("db.db.insert_abonnement_notif")
    def test_abonner(self, mock_insert):
        obs = Observateur(self.acheteur, {"taille": "M"})
        result = self.observable.abonner(obs)
        self.assertTrue(result)
        self.assertIn(obs, self.observable._observateurs)
        mock_insert.assert_called_once()

    @patch("db.db.insert_abonnement_notif")
    def test_abonner_doublon(self, mock_insert):
        """S'abonner deux fois avec le même observateur retourne False."""
        obs = Observateur(self.acheteur, {"taille": "M"})
        self.observable.abonner(obs)
        result = self.observable.abonner(obs)
        self.assertFalse(result)
        self.assertEqual(len(self.observable._observateurs), 1)

    @patch("db.db.delete_abonnement_notif")
    @patch("db.db.insert_abonnement_notif")
    def test_desabonner(self, mock_insert, mock_delete):
        obs = Observateur(self.acheteur, {"taille": "M"})
        self.observable.abonner(obs)
        result = self.observable.desabonner(obs)
        self.assertTrue(result)
        self.assertNotIn(obs, self.observable._observateurs)
        mock_delete.assert_called_once()

    @patch("db.db.insert_abonnement_notif")
    def test_notifier_dispatche_tous(self, mock_insert):
        """notifier() appelle update() sur chaque observateur."""
        acheteur2 = _make_acheteur(id=2, pseudo="bob")
        plateforme1 = MagicMock()
        plateforme1.notifications = []
        plateforme2 = MagicMock()
        plateforme2.notifications = []

        obs1 = Observateur(self.acheteur, {"taille": "M"}, plateforme1)
        obs2 = Observateur(acheteur2, {"couleur": "Bleu"}, plateforme2)
        self.observable.abonner(obs1)
        self.observable.abonner(obs2)

        article = _make_article(taille="M", couleur="Bleu")
        self.observable.notifier(article)

        self.assertIn(article, plateforme1.notifications)
        self.assertIn(article, plateforme2.notifications)

    def test_notifier_liste_vide(self):
        """notifier() sans observateurs ne lève pas d'erreur."""
        article = _make_article()
        try:
            self.observable.notifier(article)
        except Exception as e:
            self.fail(f"notifier() a levé une exception : {e}")


if __name__ == "__main__":
    unittest.main()

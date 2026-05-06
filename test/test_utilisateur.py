import unittest
from models.utilisateur import Utilisateur, Vendeur, Acheteur


class TestUtilisateur(unittest.TestCase):

    def setUp(self):
        # Crée un utilisateur de test réutilisable
        self.user = Utilisateur(1, "alice", "alice@mail.com", ...)

    def test_creation(self):
        self.assertEqual(self.user.pseudo, "alice")


if __name__ == '__main__':
    unittest.main()
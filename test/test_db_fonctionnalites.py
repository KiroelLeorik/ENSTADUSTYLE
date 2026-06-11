"""Tests unitaires pour les fonctions DB ajoutées — Author : LARDILLIER Léo"""

import unittest
import sqlite3
from unittest.mock import patch, MagicMock


# ── BDD en mémoire ────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS Utilisateurs (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT, nom TEXT, prenom TEXT, mail TEXT,
    mot_de_passe TEXT, est_pro INTEGER, evaluation REAL,
    localisation TEXT, date_inscription TEXT
);
CREATE TABLE IF NOT EXISTS Objets (
    id_objet INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, description TEXT, categorie TEXT,
    sous_categorie TEXT, genre TEXT, taille TEXT,
    couleur TEXT, marque TEXT, etat TEXT,
    prix_vendeur REAL, prix_min REAL, id_vendeur INTEGER,
    photo TEXT, matiere TEXT, vendu INTEGER DEFAULT 0,
    date_publication TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS Favoris (
    id_favori INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER, id_objet INTEGER
);
CREATE TABLE IF NOT EXISTS Abonnements (
    id_abonnement INTEGER PRIMARY KEY AUTOINCREMENT,
    id_abonne INTEGER NOT NULL, id_suivi INTEGER NOT NULL,
    date_abonnement TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_abonne, id_suivi)
);
CREATE TABLE IF NOT EXISTS Transactions (
    id_transaction INTEGER PRIMARY KEY AUTOINCREMENT,
    id_acheteur INTEGER, id_vendeur INTEGER, id_objet INTEGER,
    prix_propose REAL, prix_final REAL, statut TEXT
);
CREATE TABLE IF NOT EXISTS Abonnements_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_acheteur INTEGER, criteres TEXT,
    date_abonnement TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    return conn


class _NoClose:
    """Wrapper qui empêche close() de fermer la connexion in-memory entre deux appels DB."""
    def __init__(self, conn):
        self._conn = conn
    def __getattr__(self, name):
        return getattr(self._conn, name)
    def close(self):
        pass


def _patch_conn(conn):
    """Retourne un patcher qui injecte conn dans db.db.get_connection."""
    wrapped = _NoClose(conn)
    return patch("db.db.get_connection", return_value=wrapped)


def seed_article(conn, id_objet=1):
    conn.execute("""INSERT INTO Objets (id_objet, nom, description, categorie,
        sous_categorie, genre, taille, couleur, marque, etat,
        prix_vendeur, prix_min, id_vendeur, photo, matiere, vendu)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (id_objet, "Veste test", "desc", "Vêtements",
         "Vestes", "Femme", "M", "Bleu", "Zara", "bon",
         30.0, 20.0, 1, None, "Coton", 0))
    conn.commit()


def seed_user(conn, id_utilisateur=1):
    conn.execute("""INSERT INTO Utilisateurs (id_utilisateur, pseudo, nom, prenom,
        mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (id_utilisateur, "alice92", "Martin", "Alice",
         "alice@mail.com", "pwd", 0, 4.8, "Paris", "2026-01-01"))
    conn.commit()


# ── Tests abonnements sociaux ─────────────────────────────────────────────────

class TestAbonnements(unittest.TestCase):

    def setUp(self):
        self.conn = make_conn()
        self.patcher = _patch_conn(self.conn)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.conn.close()

    def test_insert_abonnement(self):
        from db.db import insert_abonnement
        insert_abonnement(1, 2)
        c = self.conn.execute("SELECT COUNT(*) FROM Abonnements WHERE id_abonne=1 AND id_suivi=2")
        self.assertEqual(c.fetchone()[0], 1)

    def test_insert_abonnement_idempotent(self):
        """INSERT OR IGNORE : deux fois le même abonnement → 1 seule ligne."""
        from db.db import insert_abonnement
        insert_abonnement(1, 2)
        insert_abonnement(1, 2)
        c = self.conn.execute("SELECT COUNT(*) FROM Abonnements")
        self.assertEqual(c.fetchone()[0], 1)

    def test_delete_abonnement(self):
        from db.db import insert_abonnement, delete_abonnement
        insert_abonnement(1, 2)
        delete_abonnement(1, 2)
        c = self.conn.execute("SELECT COUNT(*) FROM Abonnements")
        self.assertEqual(c.fetchone()[0], 0)

    def test_is_abonne_vrai(self):
        from db.db import insert_abonnement, is_abonne
        insert_abonnement(1, 2)
        self.assertTrue(is_abonne(1, 2))

    def test_is_abonne_faux(self):
        from db.db import is_abonne
        self.assertFalse(is_abonne(1, 99))

    def test_is_abonne_non_symetrique(self):
        """1 suit 2 ne signifie pas que 2 suit 1."""
        from db.db import insert_abonnement, is_abonne
        insert_abonnement(1, 2)
        self.assertFalse(is_abonne(2, 1))

    def test_get_nb_abonnes(self):
        from db.db import insert_abonnement, get_nb_abonnes
        insert_abonnement(1, 3)
        insert_abonnement(2, 3)
        self.assertEqual(get_nb_abonnes(3), 2)

    def test_get_nb_abonnements(self):
        from db.db import insert_abonnement, get_nb_abonnements
        insert_abonnement(1, 2)
        insert_abonnement(1, 3)
        self.assertEqual(get_nb_abonnements(1), 2)


# ── Tests favoris ─────────────────────────────────────────────────────────────

class TestFavoris(unittest.TestCase):

    def setUp(self):
        self.conn = make_conn()
        self.patcher = _patch_conn(self.conn)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.conn.close()

    def test_insert_favori(self):
        from db.db import insert_favori
        insert_favori(1, 10)
        c = self.conn.execute("SELECT COUNT(*) FROM Favoris WHERE id_utilisateur=1 AND id_objet=10")
        self.assertEqual(c.fetchone()[0], 1)

    def test_delete_favori(self):
        from db.db import insert_favori, delete_favori
        insert_favori(1, 10)
        delete_favori(1, 10)
        c = self.conn.execute("SELECT COUNT(*) FROM Favoris")
        self.assertEqual(c.fetchone()[0], 0)

    def test_get_favoris(self):
        from db.db import insert_favori, get_favoris
        insert_favori(1, 10)
        insert_favori(1, 20)
        result = get_favoris(1)
        self.assertEqual(len(result), 2)

    def test_get_favoris_vide(self):
        from db.db import get_favoris
        self.assertEqual(get_favoris(99), [])


# ── Tests update_article ──────────────────────────────────────────────────────

class TestUpdateArticle(unittest.TestCase):

    def setUp(self):
        self.conn = make_conn()
        seed_article(self.conn)
        self.patcher = _patch_conn(self.conn)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.conn.close()

    def test_update_nom(self):
        from db.db import update_article
        update_article(1, "Nouveau nom", "desc", 40.0, 25.0, "neuf",
                       "Vestes", "Femme", "L", "Rouge", "Zara", "Coton", None)
        c = self.conn.execute("SELECT nom FROM Objets WHERE id_objet=1")
        self.assertEqual(c.fetchone()[0], "Nouveau nom")

    def test_update_prix(self):
        from db.db import update_article
        update_article(1, "Veste test", "desc", 99.0, 50.0, "bon",
                       "Vestes", "Femme", "M", "Bleu", "Zara", "Coton", None)
        c = self.conn.execute("SELECT prix_vendeur, prix_min FROM Objets WHERE id_objet=1")
        row = c.fetchone()
        self.assertEqual(row[0], 99.0)
        self.assertEqual(row[1], 50.0)

    def test_update_photo(self):
        from db.db import update_article
        update_article(1, "Veste test", "desc", 30.0, 20.0, "bon",
                       "Vestes", "Femme", "M", "Bleu", "Zara", "Coton",
                       "assets/photos/veste.jpg")
        c = self.conn.execute("SELECT photo FROM Objets WHERE id_objet=1")
        self.assertEqual(c.fetchone()[0], "assets/photos/veste.jpg")


# ── Tests migration photo utilisateur ────────────────────────────────────────

class TestMigration(unittest.TestCase):

    def setUp(self):
        self.conn = make_conn()
        self.patcher = _patch_conn(self.conn)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.conn.close()

    def test_migrer_ajoute_colonne(self):
        """La migration ajoute la colonne photo si absente."""
        from db.db import migrer_photo_utilisateur
        # Supprimer la colonne photo si elle existe (recréer sans elle)
        self.conn.execute("DROP TABLE IF EXISTS Utilisateurs")
        self.conn.execute("""CREATE TABLE Utilisateurs (
            id_utilisateur INTEGER PRIMARY KEY, pseudo TEXT)""")
        self.conn.commit()
        migrer_photo_utilisateur()
        cols = [r[1] for r in self.conn.execute("PRAGMA table_info(Utilisateurs)")]
        self.assertIn("photo", cols)

    def test_migrer_idempotente(self):
        """Appeler la migration deux fois ne lève pas d'erreur."""
        from db.db import migrer_photo_utilisateur
        try:
            migrer_photo_utilisateur()
            migrer_photo_utilisateur()
        except Exception as e:
            self.fail(f"Migration a levé une exception : {e}")


# ── Tests update_utilisateur_photo ───────────────────────────────────────────

class TestUpdateUtilisateurPhoto(unittest.TestCase):

    def setUp(self):
        self.conn = make_conn()
        self.conn.execute("ALTER TABLE Utilisateurs ADD COLUMN photo TEXT")
        seed_user(self.conn)
        self.patcher = _patch_conn(self.conn)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.conn.close()

    def test_update_photo(self):
        from db.db import update_utilisateur_photo
        update_utilisateur_photo(1, "assets/photos/avatar.jpg")
        c = self.conn.execute("SELECT photo FROM Utilisateurs WHERE id_utilisateur=1")
        self.assertEqual(c.fetchone()[0], "assets/photos/avatar.jpg")


if __name__ == "__main__":
    unittest.main()

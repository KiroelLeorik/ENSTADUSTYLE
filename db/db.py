""" ----------- Author : LARDILLIER Léo ------------- """
#kkk
import sqlite3
import os
from typing import List, Tuple, Optional

def get_connection() -> sqlite3.Connection:
    """
    Ouvre et retourne une connexion SQLite vers la base de données marche.db.

    :return: objet sqlite3.Connection vers marche.db
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(BASE_DIR, "../db/marche.db"))
    return conn

def get_all_articles() -> List[Tuple]:
    """
    Récupère tous les articles présents dans la table Objets.

    :return: liste de tuples représentant chaque article de la base de données
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Objets')
    resultat = c.fetchall()
    conn.close()
    return resultat

def get_article_by_id(id: int) -> Optional[Tuple]:
    """
    Récupère un article spécifique depuis la table Objets via son identifiant.

    :param id: identifiant unique de l'article recherché
    :return: tuple contenant les données de l'article, ou None s'il n'existe pas
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Objets WHERE id_objet = ?', (id,))
    resultat = c.fetchone()
    conn.close()
    return resultat

def get_all_utilisateurs() -> List[Tuple]:
    """
    Récupère tous les utilisateurs présents dans la table Utilisateurs.

    :return: liste de tuples représentant chaque utilisateur de la base de données
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Utilisateurs')
    resultat = c.fetchall()
    conn.close()
    return resultat

def get_utilisateur_by_id(id: int) -> Optional[Tuple]:
    """
    Récupère un utilisateur spécifique depuis la table Utilisateurs via son identifiant.

    :param id: identifiant unique de l'utilisateur recherché
    :return: tuple contenant les données de l'utilisateur, ou None s'il n'existe pas
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Utilisateurs WHERE id_utilisateur = ?', (id,))
    resultat = c.fetchone()
    conn.close()
    return resultat

def insert_utilisateur(pseudo: str, nom: str, prenom: str, mail: str, mot_de_passe: str,
                       est_pro: bool, evaluation: float, localisation: Optional[str]) -> int:
    """
    Insère un nouvel utilisateur dans la table Utilisateurs.

    :param pseudo: nom d'utilisateur unique
    :param nom: nom de famille
    :param prenom: prénom
    :param mail: adresse e-mail
    :param mot_de_passe: mot de passe (non hashé)
    :param est_pro: True si l'utilisateur est un vendeur professionnel
    :param evaluation: note moyenne attribuée par la communauté (0 à 5)
    :param localisation: ville ou région de l'utilisateur
    :return: identifiant auto-généré du nouvel utilisateur
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
            INSERT INTO Utilisateurs (pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation))
    new_id = c.lastrowid  # récupère l'id généré par SQLite
    conn.commit()
    conn.close()
    return new_id

def insert_article(nom: str, description: str, categorie: str, sous_categorie: Optional[str],
                   genre: Optional[str], taille: Optional[str], couleur: Optional[str],
                   marque: Optional[str], etat: str, prix_vendeur: float, prix_min: float,
                   id_vendeur: int, photo: Optional[str], matiere: Optional[str]) -> None:
    """
    Insère un nouvel article dans la table Objets.
    La date de publication est automatiquement horodatée par SQLite.

    :param nom: nom de l'article
    :param description: description rédigée par le vendeur
    :param categorie: catégorie principale (ex. Vêtements)
    :param sous_categorie: sous-catégorie (ex. Vestes, Jeans)
    :param genre: genre cible (Homme, Femme, Unisexe)
    :param taille: taille du vêtement (XS, S, M, L, XL, XXL)
    :param couleur: couleur principale de l'article
    :param marque: marque du vêtement
    :param etat: état de l'article (neuf, tres_bon, bon, acceptable)
    :param prix_vendeur: prix affiché par le vendeur
    :param prix_min: prix minimum en dessous duquel le vendeur refuse de vendre
    :param id_vendeur: identifiant du vendeur propriétaire de l'article
    :param photo: chemin vers l'image de l'article
    :param matiere: matière principale (Coton, Jean, Laine, etc.)
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO Objets (nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, photo, matiere) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, photo, matiere))
    conn.commit()
    conn.close()
    #Remarque, pas besoin de date_de_publication car il y a un timestamp d'autoincrémenter

def update_article_vendu(id_objet: int) -> None:
    """
    Marque un article comme vendu dans la table Objets.

    :param id_objet: identifiant unique de l'article à marquer comme vendu
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE Objets SET vendu = 1 WHERE id_objet = ?', (id_objet,))
    conn.commit()
    conn.close()

def insert_transaction(id_acheteur: int, id_vendeur: int, id_objet: int,
                       prix_propose: float, prix_final: Optional[float], statut: str) -> None:
    """
    Enregistre une tentative d'achat dans la table Transactions.

    :param id_acheteur: identifiant de l'acheteur
    :param id_vendeur: identifiant du vendeur
    :param id_objet: identifiant de l'article concerné
    :param prix_propose: prix proposé par l'acheteur
    :param prix_final: prix de vente définitif (None si statut est 'negociation' ou 'refusee')
    :param statut: résultat de la transaction ('acceptee', 'negociation' ou 'refusee')
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO Transactions (id_acheteur, id_vendeur, id_objet, prix_propose, prix_final, statut) VALUES (?, ?, ?, ?, ?, ?)', (id_acheteur, id_vendeur, id_objet, prix_propose, prix_final, statut))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(get_all_articles())
    print(get_all_utilisateurs())
    print(get_utilisateur_by_id(1))
    print(get_article_by_id(1))

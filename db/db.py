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
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id
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

def delete_article(id_objet: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM Objets WHERE id_objet = ?', (id_objet,))
    conn.commit()
    conn.close()

def update_utilisateur(id: int, pseudo: str = None, mail: str = None,
                       localisation: str = None) -> None:
    conn = get_connection()
    c = conn.cursor()
    if pseudo is not None:
        c.execute('UPDATE Utilisateurs SET pseudo = ? WHERE id_utilisateur = ?', (pseudo, id))
    if mail is not None:
        c.execute('UPDATE Utilisateurs SET mail = ? WHERE id_utilisateur = ?', (mail, id))
    if localisation is not None:
        c.execute('UPDATE Utilisateurs SET localisation = ? WHERE id_utilisateur = ?', (localisation, id))
    conn.commit()
    conn.close()

def update_mot_de_passe(id: int, nouveau_mdp: str) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE Utilisateurs SET mot_de_passe = ? WHERE id_utilisateur = ?', (nouveau_mdp, id))
    conn.commit()
    conn.close()

def update_article(id_objet: int, nom: str, description: str, prix_vendeur: float,
                   prix_min: float, etat: str, sous_categorie: str = None,
                   genre: str = None, taille: str = None, couleur: str = None,
                   marque: str = None, matiere: str = None, photo: str = None) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE Objets SET nom=?, description=?, prix_vendeur=?, prix_min=?,
                 etat=?, sous_categorie=?, genre=?, taille=?, couleur=?, marque=?, matiere=?,
                 photo=? WHERE id_objet=?''',
              (nom, description, prix_vendeur, prix_min, etat, sous_categorie,
               genre, taille, couleur, marque, matiere, photo, id_objet))
    conn.commit()
    conn.close()

def migrer_photo_utilisateur() -> None:
    conn = get_connection()
    c = conn.cursor()
    cols = [r[1] for r in c.execute("PRAGMA table_info(Utilisateurs)").fetchall()]
    if "photo" not in cols:
        c.execute("ALTER TABLE Utilisateurs ADD COLUMN photo TEXT")
        conn.commit()
    conn.close()

def update_utilisateur_photo(id: int, photo: str) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE Utilisateurs SET photo = ? WHERE id_utilisateur = ?', (photo, id))
    conn.commit()
    conn.close()

def insert_favori(id_utilisateur, id_objet):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO Favoris (id_utilisateur, id_objet) VALUES (?, ?)', (id_utilisateur, id_objet))
    conn.commit()
    conn.close()

def delete_favori(id_utilisateur, id_objet):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM Favoris WHERE id_utilisateur = ? AND id_objet = ?', (id_utilisateur, id_objet))
    conn.commit()
    conn.close()

def get_favoris(id_utilisateur):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Favoris WHERE id_utilisateur = ?', (id_utilisateur,))
    resultat = c.fetchall()
    conn.close()
    return resultat

def insert_abonnement_notif(id_acheteur, criteres):
    import json
    criterias = json.dumps(criteres)
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO Abonnements_notifications (id_acheteur, criteres) VALUES (?, ?)', (id_acheteur, criterias))
    conn.commit()
    conn.close()

def delete_abonnement_notif(id_acheteur, criteres):
    import json
    criterias = json.dumps(criteres)
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM Abonnements_notifications WHERE id_acheteur = ? AND criteres = ?', (id_acheteur, criterias))
    conn.commit()
    conn.close()

def get_all_abonnements_notif():
    import json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Abonnements_notifications')
    resultat = c.fetchall()
    conn.close()
    return [[r[0], r[1], json.loads(r[2]), r[3]] for r in resultat]

def get_abonnements_notif(id_acheteur):
    import json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Abonnements_notifications WHERE id_acheteur = ?', (id_acheteur,))
    resultat = c.fetchall()
    conn.close()
    resultat_json = []
    for r in resultat:
        resultat_json.append([r[0], r[1], json.loads(r[2]), r[3]])
    return resultat_json

def get_nb_abonnes(id_utilisateur):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM Abonnements WHERE id_suivi = ?', (id_utilisateur,))
    result = c.fetchone()[0]
    conn.close()
    return result

def get_nb_abonnements(id_utilisateur):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM Abonnements WHERE id_abonne = ?', (id_utilisateur,))
    result = c.fetchone()[0]
    conn.close()
    return result

def insert_abonnement(id_abonne: int, id_suivi: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO Abonnements (id_abonne, id_suivi) VALUES (?, ?)', (id_abonne, id_suivi))
    conn.commit()
    conn.close()

def delete_abonnement(id_abonne: int, id_suivi: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM Abonnements WHERE id_abonne = ? AND id_suivi = ?', (id_abonne, id_suivi))
    conn.commit()
    conn.close()

def is_abonne(id_abonne: int, id_suivi: int) -> bool:
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM Abonnements WHERE id_abonne = ? AND id_suivi = ?', (id_abonne, id_suivi))
    result = c.fetchone() is not None
    conn.close()
    return result


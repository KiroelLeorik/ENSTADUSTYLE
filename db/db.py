""" ----------- Author : LARDILLIER Léo ------------- """

import sqlite3
import os

def get_connection():
    """
    Connection à la base de données
    :return: une variable qui stocke la BDD
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(BASE_DIR, "../db/marche.db"))
    return conn
def get_all_articles():
    """
    :return: Tout les articles présent dans la BDD
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Objets')
    resultat = c.fetchall()
    conn.close()
    return resultat
def get_article_by_id(id):
    """

    :param id: identifiant de l'article recherché
    :return: les détails de l'article trouvé par id
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Objets WHERE id_objet = ?', (id,))
    resultat = c.fetchone()
    conn.close()
    return resultat
def get_all_utilisateurs():
    """

    :return:
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Utilisateurs')
    resultat = c.fetchall()
    conn.close()
    return resultat
def get_utilisateur_by_id(id):
    """

    :param id:
    :return:
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Utilisateurs WHERE id_utilisateur = ?', (id,))
    resultat = c.fetchone()
    conn.close()
    return resultat
#persistance BDD
def insert_utilisateur(pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation):
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

def insert_article(nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, photo, matiere):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO Objets (nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, photo, matiere) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (nom, description, categorie, sous_categorie, genre, taille, couleur, marque, etat, prix_vendeur, prix_min, id_vendeur, photo, matiere))
    conn.commit()
    conn.close()
    #Remarque, pas besoin de date_de_publication car il y a un timestamp d'autoincrémenter
def update_article_vendu(id_objet):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE Objets SET vendu = 1 WHERE id_objet = ?', (id_objet,))
    conn.commit()
    conn.close()
def insert_transaction(id_acheteur, id_vendeur, id_objet, prix_propose, prix_final, statut):
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



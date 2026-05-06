import sqlite3
import os

def get_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(BASE_DIR, "../db/marche.db"))
    return conn
def get_all_articles():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Objets')
    resultat = c.fetchall()
    conn.close()
    return resultat
def get_article_by_id(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Objets WHERE id_objet = ?', (id,))
    resultat = c.fetchone()
    conn.close()
    return resultat
def get_all_utilisateurs():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Utilisateurs')
    resultat = c.fetchall()
    conn.close()
    return resultat
def get_utilisateur_by_id(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Utilisateurs WHERE id_utilisateur = ?', (id,))
    resultat = c.fetchone()
    conn.close()
    return resultat

if __name__ == "__main__":
    print(get_all_articles())
    print(get_all_utilisateurs())
    print(get_utilisateur_by_id(1))
    print(get_article_by_id(1))



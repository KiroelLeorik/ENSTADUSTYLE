""" ----------- Author : GREGOIRE Louna ------------- """
import time
from services.recherche import rechercher, scorer_articles, scorer_articles_python
from db.db import *
from models.article import Vetement
if __name__ == '__main__':

    articles = get_all_articles()
    vetements = [Vetement(*a) for a in articles]
    criteres = {"sous_categorie": "Vestes", "couleur": "Bleu", "taille": "M", "genre": "Homme"}

    # Simuler 100 000 articles
    gros_vetements = vetements * 5000  # 20 × 5000 = 100 000 articles

    start = time.time() #on calcule le temps que met la fonction rechercher pour rechercher les produits qui correspondent aux critères parmis 10000 vêtements
    for _ in range(10):
        rechercher(gros_vetements, criteres)
    temps_python = time.time() - start
    print(f"Fonction Rechercher (100k articles) : {temps_python:.4f}s")

    start = time.time()
    for _ in range(10):    #on calcule le temps que met la fonction scorer_articles_python pour scorer 10000 vêtements selon les critères imposés
        scorer_articles_python(gros_vetements, criteres)
    temps = time.time() - start
    print(f"Scorer Python : {temps:.4f}s")

    start = time.time()
    for _ in range(10):
        scorer_articles(gros_vetements, criteres)
    temps = time.time() - start
    print(f"Scorer NumPy :  {temps:.4f}s")

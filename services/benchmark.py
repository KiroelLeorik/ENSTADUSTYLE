import time
from services.recherche import rechercher, scorer_articles, scorer_articles_python
from db.db import *
from models.article import Vetement
if __name__ == '__main__':

    articles = get_all_articles()
    vetements = [Vetement(*a) for a in articles]
    criteres = {"sous_categorie": "Vestes", "couleur": "Bleu", "taille": "M", "genre": "Homme"}
    """
    start = time.time()
    for _ in range(1000000):
        test = scorer_articles(vetements, criteres)
    temps = time.time() - start

    print(f"Temps : {temps:.4f}s pour l'algo scorer_articles")

    start = time.time()
    for _ in range(1000000):
        test = rechercher(vetements, criteres)
    temps = time.time() - start
    print(f"Temps : {temps:.4f}s pour l'algo rechercher")
    """
    # Simuler 100 000 articles
    gros_vetements = vetements * 5000  # 20 × 5000 = 100 000 articles

    start = time.time()
    for _ in range(10):
        scorer_articles(gros_vetements, criteres)
    temps_numpy = time.time() - start
    print(f"NumPy (100k articles) : {temps_numpy:.4f}s")

    start = time.time()
    for _ in range(10):
        rechercher(gros_vetements, criteres)
    temps_python = time.time() - start
    print(f"Python (100k articles) : {temps_python:.4f}s")

    start = time.time()
    for _ in range(10):
        scorer_articles_python(gros_vetements, criteres)
    temps = time.time() - start
    print(f"Scorer Python : {temps:.4f}s")

    start = time.time()
    for _ in range(10):
        scorer_articles(gros_vetements, criteres)
    temps = time.time() - start
    print(f"Scorer NumPy :  {temps:.4f}s")

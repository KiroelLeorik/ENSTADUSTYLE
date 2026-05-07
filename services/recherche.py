import numpy as np


def scorer_articles(articles, criteres):
    n = len(criteres)
    poids = np.array([1/n for i in range(n)])  # quels poids pour chaque critère ?
    categorie = criteres.get('categorie')
    sous_categorie = criteres.get('sous_categorie')
    genre = criteres.get('genre')
    taille = criteres.get('taille')
    couleur = criteres.get('couleur')
    marque = criteres.get('marque')
    etat = criteres.get('etat')
    prix = criteres.get('prix')
    matiere = criteres.get('matiere')
    resultats = []
    if articles.vendu:
        return 0
    for a in articles:
        scores = np.array([
            1.0 if categorie is not None and a.categorie != categorie else 0.0, # critère 1
            1.0 if sous_categorie is not None and a.sous_categorie != sous_categorie else 0.0,
            if genre is not None and a.genre != genre else 0.0,
            1.0 if sous_categorie is not None and a.sous_categorie != sous_categorie else 0.0,
            1.0 if sous_categorie is not None and a.sous_categorie != sous_categorie else 0.0,
            1.0 if sous_categorie is not None and a.sous_categorie != sous_categorie else 0.0,
            1.0 if sous_categorie is not None and a.sous_categorie != sous_categorie else 0.0,
        ])
        score = np.dot(scores, poids)  # produit scalaire
    return score
def rechercher(articles, criteres):
    resultats = []
    categorie = criteres.get('categorie')
    sous_categorie = criteres.get('sous_categorie')
    genre = criteres.get('genre')
    taille = criteres.get('taille')
    couleur = criteres.get('couleur')
    marque = criteres.get('marque')
    etat = criteres.get('etat')
    prix = criteres.get('prix')
    matiere = criteres.get('matiere')
    for a in articles:
        check = True
        if a.vendu:
            check = False
        if categorie is not None and a.categorie != categorie:
            check = False
        if sous_categorie is not None and a.sous_categorie != sous_categorie:
            check = False
        if genre is not None and a.genre != genre:
            check = False
        if taille is not None and a.taille != taille:
            check = False
        if couleur is not None and a.couleur != couleur:
            check = False
        if marque is not None and a.marque != marque:
            check = False
        if etat is not None and a.etat != etat:
            check = False
        if prix is not None and prix < a.prix_vendeur:
            check = False
        if matiere is not None and a.matiere != matiere:
            check = False
        if check:
            resultats.append(a)
    return resultats
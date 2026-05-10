import numpy as np


def scorer_articles(articles, criteres):
    #INIT
    resultat = []
    mapping = {
        "categorie": "categorie",
        "sous_categorie": "sous_categorie",
        "genre": "genre",
        "taille": "taille",
        "couleur": "couleur",
        "marque": "marque",
        "etat": "etat",
        "matiere": "matiere",
    }
    criteres_actifs = {k : v for k, v in criteres.items() if k in mapping}
    if not criteres_actifs:
        return articles

    articles_dispo = [a for a in articles if not a.vendu]
    cles = list(criteres_actifs)
    n = len(cles)
    poid = np.array([1/n] * n)
    matrice = []

    for a in articles_dispo:
        ligne = []
        for cle in cles:
            if getattr(a, cle) == criteres_actifs[cle]:
                ligne.append(1.0)
            else:
                ligne.append(0.0)
        matrice.append(ligne)

    matrice = np.array(matrice)
    scores = matrice @ poid

    return resultat


"""---------------------- OLD ------------------------------------------
Version lente qui ne sort pas une liste triée en fonction du score mais qui sort seulement les articles qui correspondent exactement aux
critères.
La version calcul matriciel ci-dessous est plus rapide et permet de trier les résultats en fonction du score obtenu.
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
"""

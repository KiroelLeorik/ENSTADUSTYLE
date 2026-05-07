

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
    for article in articles:
        check = True
        if article.vendu:
            check = False
        if categorie is not None and article.categorie != categorie:
            check = False
        if sous_categorie is not None and article.sous_categorie != sous_categorie:
            check = False
        if genre is not None and article.genre != genre:
            check = False
        if taille is not None and article.taille != taille:
            check = False
        if couleur is not None and article.couleur != couleur:
            check = False
        if marque is not None and article.marque != marque:
            check = False
        if etat is not None and article.etat != etat:
            check = False
        if prix is not None and prix < article.prix_vendeur:
            check = False
        if matiere is not None and article.matiere != matiere:
            check = False
        if check:
            resultats.append(article)
    return resultats